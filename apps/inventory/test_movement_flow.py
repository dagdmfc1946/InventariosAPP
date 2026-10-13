from unittest.mock import patch
import time
import uuid
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse
from apps.components.models import Category, Component
from .models import Stock, StockMovement
from .forms_movement import MovementForm


class MovementFlowTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser('movimientos', password='Test-9812!')
        self.client.force_login(self.user)
        self.component = Component.objects.create(category=Category.objects.create(name='Sensores'), reference='S1', name='Sensor')
        self.stock = Stock.objects.create(component=self.component, quantity=10, maximum_quantity=30)
        self.url = reverse('component_movement', args=[self.component.pk])

    def data(self, **kwargs):
        result = {'token': MovementForm(component=self.component, user=self.user).initial['token'],
                  'movement_type': 'exit', 'quantity': '3', 'reason': 'Uso en proyecto', 'action': 'register'}
        result.update(kwargs)
        return result

    def test_preview_does_not_write_and_repeated_submit_does_not_repeat(self):
        data = self.data()
        response = self.client.post(self.url, {**data, 'action': 'preview'})
        self.assertContains(response, '7 unidades')
        self.assertFalse(StockMovement.objects.exists())
        for _ in range(2):
            self.assertEqual(self.client.post(self.url, data).status_code, 302)
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.quantity, 7)
        self.assertEqual(StockMovement.objects.count(), 1)

    def test_invalid_negative_zero_overdraft_and_maximum_are_rejected(self):
        for kind, quantity in [('exit', 11), ('entry', -2), ('adjustment', -11), ('entry', 21), ('adjustment', 0)]:
            self.assertEqual(self.client.post(self.url, self.data(movement_type=kind, quantity=quantity)).status_code, 200)
        self.assertFalse(StockMovement.objects.exists())
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.quantity, 10)

    def test_stale_saldo_tampered_token_and_missing_reason_cannot_write(self):
        data = self.data()
        StockMovement.objects.create(stock=self.stock, movement_type='entry', quantity=1)
        response = self.client.post(self.url, data)
        self.assertContains(response, 'El saldo cambió')
        self.assertEqual(self.client.post(self.url, self.data(token='false')).status_code, 200)
        self.assertEqual(self.client.post(self.url, self.data(reason='')).status_code, 200)
        self.assertEqual(StockMovement.objects.count(), 1)

    def test_adjustment_and_atomic_failure(self):
        data = self.data(movement_type='adjustment', quantity=-2)
        self.assertEqual(self.client.post(self.url, data).status_code, 302)
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.quantity, 8)
        self.assertEqual(StockMovement.objects.get().quantity, -2)
        with patch('django.db.models.Model.save', side_effect=ValidationError('Fallo de inserción')):
            self.assertEqual(self.client.post(self.url, self.data(movement_type='entry', quantity=2)).status_code, 200)
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.quantity, 8)

    def test_permissions_and_csrf(self):
        normal = get_user_model().objects.create_user('lector')
        self.client.force_login(normal)
        self.assertEqual(self.client.post(self.url, self.data()).status_code, 403)
        csrf = Client(enforce_csrf_checks=True)
        csrf.force_login(self.user)
        self.assertEqual(csrf.post(self.url, self.data()).status_code, 403)

    def test_reusing_operation_for_other_component_or_changed_values_is_rejected(self):
        data = self.data()
        self.client.post(self.url, data)
        self.assertContains(self.client.post(self.url, {**data, 'quantity': 1}), 'ya se utilizó')
        other = Component.objects.create(category=self.component.category, reference='S2', name='Otro')
        self.assertContains(self.client.post(reverse('component_movement', args=[other.pk]), data), 'no corresponde')
        self.assertEqual(StockMovement.objects.count(), 1)

    def test_repeated_large_exit_and_unknown_action(self):
        data = self.data(quantity=7)
        self.assertEqual(self.client.post(self.url, {**data, 'action': 'unknown'}).status_code, 200)
        for _ in range(2):
            self.assertEqual(self.client.post(self.url, data).status_code, 302)
        self.assertEqual(Stock.objects.get(pk=self.stock.pk).quantity, 3)
        self.assertEqual(StockMovement.objects.count(), 1)

    def test_complete_history_is_paginated_on_component(self):
        for _ in range(26):
            StockMovement.objects.create(stock=self.stock, movement_type='adjustment', quantity=-1 if _ % 2 else 1)
        response = self.client.get(reverse('component_detail', args=[self.component.pk]), {'movements_page': 2})
        self.assertEqual(response.context['movements'].paginator.count, 26)
        self.assertEqual(len(response.context['movements']), 1)

    def test_missing_stock_created_at_zero_before_entry(self):
        other = Component.objects.create(category=self.component.category, reference='S2', name='Sin existencias')
        data = self.data(movement_type='entry', quantity=4)
        data['token'] = MovementForm(component=other, user=self.user).initial['token']
        self.assertEqual(self.client.post(reverse('component_movement', args=[other.pk]), data).status_code, 302)
        self.assertEqual(Stock.objects.get(component=other).quantity, 4)

    def test_expired_token_and_other_session_cannot_write(self):
        data = self.data()
        with patch('django.core.signing.time.time', return_value=time.time() + 3601):
            self.assertContains(self.client.post(self.url, data), 'formulario venció')
        other = get_user_model().objects.create_superuser('otra_sesion', password='Test-7394!')
        self.client.force_login(other)
        self.assertContains(self.client.post(self.url, data), 'no corresponde')
        self.assertFalse(StockMovement.objects.exists())

    def test_operation_identifier_is_immutable(self):
        self.client.post(self.url, self.data())
        movement = StockMovement.objects.get()
        movement.request_id = uuid.uuid4()
        with self.assertRaises(ValidationError):
            movement.save()
