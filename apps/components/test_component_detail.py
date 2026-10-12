from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from apps.core.roles import configure_inventory_roles
from apps.inventory.models import Location, Stock
from .models import Category, Component, Specification


class ComponentDetailTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user('operator')
        self.user.groups.add(configure_inventory_roles()['operator'])
        self.client.force_login(self.user)
        self.category = Category.objects.create(name='Sensors')
        self.location = Location.objects.create(shelf='Estante A')
        self.component = Component.objects.create(category=self.category, reference='S1', name='English name')
        Stock.objects.create(component=self.component, quantity=12)
        self.data = {'category': self.category.pk, 'reference': 'S1', 'name': 'Nombre editado',
                     'location': self.location.pk, 'is_active': 'on',
                     'specifications-TOTAL_FORMS': 1, 'specifications-INITIAL_FORMS': 0,
                     'specifications-0-attribute': 'Voltaje', 'specifications-0-value': '5',
                     'specifications-0-unit': 'V'}

    def test_edit_basic_data_specs_and_location_keeps_stock(self):
        response = self.client.post(reverse('component_edit', args=[self.component.pk]), self.data)
        self.assertRedirects(response, reverse('component_detail', args=[self.component.pk]))
        self.component.refresh_from_db()
        self.assertEqual(self.component.name, 'Nombre editado')
        self.assertEqual(self.component.location, self.location)
        self.assertEqual(self.component.stock.quantity, 12)
        self.assertEqual(self.component.specifications.get().value, '5')

    def test_duplicate_specifications_do_not_partially_save(self):
        data = {**self.data, 'specifications-TOTAL_FORMS': 2,
                'specifications-1-attribute': 'Voltaje', 'specifications-1-value': '12'}
        response = self.client.post(reverse('component_edit', args=[self.component.pk]), data)
        self.assertEqual(response.status_code, 200)
        self.component.refresh_from_db()
        self.assertEqual(self.component.name, 'English name')
        self.assertFalse(self.component.specifications.exists())

    def test_category_creation_retains_pending_fields_without_saving_component(self):
        response = self.client.post(reverse('component_edit', args=[self.component.pk]), {
            **self.data, 'action': 'create_category', 'category-name': 'Nueva categoría',
        })
        self.assertContains(response, 'Nombre editado')
        self.assertTrue(Category.objects.filter(name='Nueva categoría').exists())
        self.component.refresh_from_db()
        self.assertEqual(self.component.name, 'English name')
        self.assertFalse(self.component.specifications.exists())

    def test_add_spec_row_without_javascript_retains_values(self):
        response = self.client.post(reverse('component_edit', args=[self.component.pk]), {**self.data, 'action': 'add_spec_row'})
        self.assertEqual(response.context['formset'].total_form_count(), 2)
        self.assertContains(response, 'Nombre editado')
        self.assertFalse(self.component.specifications.exists())

    def test_reader_can_read_but_cannot_edit(self):
        reader = get_user_model().objects.create_user('reader')
        reader.groups.add(configure_inventory_roles()['reader'])
        self.client.force_login(reader)
        self.assertContains(self.client.get(reverse('component_detail', args=[self.component.pk])), 'English name')
        self.assertEqual(self.client.post(reverse('component_edit', args=[self.component.pk]), self.data).status_code, 403)

    def test_location_creation_retains_component_and_specification_fields(self):
        response = self.client.post(reverse('component_edit', args=[self.component.pk]), {
            **self.data, 'action': 'create_location', 'location-box': 'Nueva caja',
        })
        self.assertContains(response, 'Nombre editado')
        self.assertContains(response, 'Voltaje')
        self.assertNotContains(response, 'Revisa los campos y las especificaciones indicadas.')
        self.assertTrue(Location.objects.filter(box='Nueva caja').exists())
        self.component.refresh_from_db()
        self.assertIsNone(self.component.location)

    def test_other_components_specification_id_cannot_be_edited(self):
        other = Component.objects.create(category=self.category, reference='OTHER', name='Otro')
        specification = Specification.objects.create(component=other, attribute='Protegido', value='12')
        response = self.client.post(reverse('component_edit', args=[self.component.pk]), {
            **self.data, 'specifications-INITIAL_FORMS': 1, 'specifications-0-id': specification.pk,
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['formset'].errors)
        specification.refresh_from_db()
        self.assertEqual(specification.value, '12')
        self.component.refresh_from_db()
        self.assertEqual(self.component.name, 'English name')

    def test_specification_deletion_is_transactional_and_stock_is_untouched(self):
        specification = Specification.objects.create(component=self.component, attribute='Voltaje', value='5')
        response = self.client.post(reverse('component_edit', args=[self.component.pk]), {
            **self.data, 'specifications-INITIAL_FORMS': 1, 'specifications-0-id': specification.pk,
            'specifications-0-DELETE': 'on', 'quantity': '999',
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Specification.objects.filter(pk=specification.pk).exists())
        self.assertEqual(Stock.objects.get(component=self.component).quantity, 12)
