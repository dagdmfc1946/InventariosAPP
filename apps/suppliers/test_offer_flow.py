from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from apps.components.models import Category, Component
from apps.core.roles import configure_inventory_roles
from .models import Supplier, SupplierOffer


class SupplierFlowTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user('operador')
        self.user.groups.add(configure_inventory_roles()['operator'])
        self.client.force_login(self.user)
        self.component = Component.objects.create(category=Category.objects.create(name='Sensores'), reference='S1', name='Sensor')
        self.supplier = Supplier.objects.create(name='Distribuidor')
        self.url = reverse('offer_create', args=[self.component.pk])
        self.data = {'supplier': self.supplier.pk, 'part_number': 'PARTE-1', 'price': '12.50', 'currency': 'cop', 'minimum_quantity': 1}

    def test_operator_creates_supplier_and_offer_then_edits(self):
        response = self.client.post(reverse('supplier_create'), {'name': 'Otro proveedor', 'email': 'contacto@example.test'})
        self.assertRedirects(response, reverse('supplier_list'))
        self.assertEqual(self.client.post(self.url, self.data).status_code, 302)
        offer = SupplierOffer.objects.get()
        self.assertEqual(offer.currency, 'COP')
        self.assertEqual(offer.component, self.component)
        response = self.client.post(reverse('offer_edit', args=[self.component.pk, offer.pk]), {**self.data, 'price': '10'})
        self.assertEqual(response.status_code, 302)
        self.assertContains(self.client.get(reverse('component_detail', args=[self.component.pk])), 'Distribuidor')

    def test_negative_price_zero_minimum_duplicate_and_cross_component_rejected(self):
        for field, value in [('price', '-1'), ('minimum_quantity', '0'), ('url', 'javascript:alert(1)')]:
            self.assertEqual(self.client.post(self.url, {**self.data, field: value}).status_code, 200)
        self.assertFalse(SupplierOffer.objects.exists())
        self.client.post(self.url, self.data)
        self.assertEqual(self.client.post(self.url, self.data).status_code, 200)
        self.assertEqual(SupplierOffer.objects.count(), 1)
        other = Component.objects.create(category=self.component.category, reference='S2', name='Otro')
        self.assertEqual(self.client.post(reverse('offer_edit', args=[other.pk, SupplierOffer.objects.get().pk]), self.data).status_code, 404)

    def test_reader_can_consult_but_cannot_write_and_supplier_identity_is_fixed(self):
        reader = get_user_model().objects.create_user('lector')
        reader.groups.add(configure_inventory_roles()['reader'])
        self.client.force_login(reader)
        self.assertEqual(self.client.get(reverse('supplier_list')).status_code, 200)
        self.assertEqual(self.client.post(self.url, self.data).status_code, 403)
        self.assertEqual(self.client.post(reverse('supplier_create'), {'name': 'Nuevo'}).status_code, 403)
        self.client.force_login(self.user)
        self.client.post(self.url, {**self.data, 'component': 99999})
        self.assertEqual(SupplierOffer.objects.get().component_id, self.component.pk)

    def test_contextual_supplier_preserves_offer_without_saving_it(self):
        self.assertNotContains(self.client.get(self.url), 'name="supplier-name" maxlength="200" required')
        response = self.client.post(self.url, {**self.data, 'action': 'create_supplier', 'supplier-name': 'Proveedor contextual'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(SupplierOffer.objects.exists())
        supplier = Supplier.objects.get(name='Proveedor contextual')
        self.assertEqual(response.context['form'].data['price'], '12.50')
        self.assertEqual(response.context['form'].data['supplier'], str(supplier.pk))
        self.assertEqual(self.client.post(self.url, {**self.data, 'supplier': supplier.pk}).status_code, 302)
        self.assertEqual(SupplierOffer.objects.get().supplier, supplier)

    def test_empty_contextual_supplier_name_remains_required_in_server(self):
        response = self.client.post(self.url, {**self.data, 'action': 'create_supplier', 'supplier-name': ''})
        self.assertIn('name', response.context['supplier_form'].errors)
        self.assertFalse(SupplierOffer.objects.exists())
