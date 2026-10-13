from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from .models import Category, Component, Specification
from apps.inventory.models import Stock, StockMovement, Location
from apps.documents.models import Datasheet
from apps.suppliers.models import Supplier, SupplierOffer


class DuplicateComponentTests(TestCase):
    def setUp(self):
        self.client.force_login(get_user_model().objects.create_superuser('duplica', password='Test-6427!'))
        self.source = Component.objects.create(category=Category.objects.create(name='Sensores'), reference='S1', name='Sensor', value='3V',
            location=Location.objects.create(box='Caja'))
        Specification.objects.create(component=self.source, attribute='Voltaje', value='3', unit='V')
        stock = Stock.objects.create(component=self.source, maximum_quantity=40)
        StockMovement.objects.create(stock=stock, quantity=12, reason='Entrada original')
        Datasheet.objects.create(component=self.source, file='datasheets/reference.pdf')
        SupplierOffer.objects.create(component=self.source, supplier=Supplier.objects.create(name='Proveedor'))
        self.url = reverse('component_duplicate', args=[self.source.pk])

    def test_copies_technical_data_without_operational_relations(self):
        response = self.client.post(self.url, {'reference': 'S2', 'name': 'Otra referencia', 'quantity': 900, 'location': self.source.location_id})
        self.assertEqual(response.status_code, 302)
        copy = Component.objects.get(reference='S2')
        self.assertEqual(copy.value, '3V')
        self.assertEqual(copy.specifications.get().attribute, 'Voltaje')
        self.assertEqual(copy.stock.quantity, 0)
        self.assertIsNone(copy.location_id)
        self.assertFalse(copy.stock.movements.exists())
        self.assertFalse(copy.datasheets.exists())
        self.assertFalse(copy.supplier_offers.exists())
        self.assertEqual(Stock.objects.get(component=self.source).quantity, 12)

    def test_same_or_existing_reference_and_specification_failure_roll_back(self):
        self.assertContains(self.client.post(self.url, {'reference': 'S1', 'name': 'Sensor'}), 'diferente')
        with patch.object(Specification, 'save', side_effect=ValidationError('Fallo técnico')):
            self.assertContains(self.client.post(self.url, {'reference': 'S2', 'name': 'Sensor'}), 'Fallo técnico')
        self.assertEqual(Component.objects.count(), 1)
        self.assertEqual(Stock.objects.count(), 1)

    def test_reader_cannot_duplicate(self):
        self.client.force_login(get_user_model().objects.create_user('lector'))
        self.assertEqual(self.client.post(self.url, {'reference': 'S2', 'name': 'Sensor'}).status_code, 403)

    def test_specification_permission_only_required_when_source_has_specs(self):
        user = get_user_model().objects.create_user('alta_basica')
        user.user_permissions.add(*Permission.objects.filter(codename__in=('add_component', 'view_component', 'add_stock')))
        self.client.force_login(user)
        self.assertNotContains(self.client.get(reverse('component_detail', args=[self.source.pk])), '>Duplicar</a>')
        self.assertEqual(self.client.post(self.url, {'reference': 'S3', 'name': 'Sensor'}).status_code, 403)
        plain = Component.objects.create(category=self.source.category, reference='S2', name='Básico')
        self.assertContains(self.client.get(reverse('component_detail', args=[plain.pk])), '>Duplicar</a>')
        self.assertEqual(self.client.post(reverse('component_duplicate', args=[plain.pk]), {'reference': 'S3', 'name': 'Otro'}).status_code, 302)
