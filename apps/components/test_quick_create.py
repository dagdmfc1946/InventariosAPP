from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
from django.test import Client, TestCase
from django.urls import reverse

from apps.components.models import Category, Component
from apps.inventory.models import Stock, StockMovement
from config.version import __version__


class QuickCreateTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Sensores')
        self.user = get_user_model().objects.create_user('operator', password='test-only')
        for app, codename in [('components', 'add_component'), ('inventory', 'add_stock'), ('inventory', 'add_stockmovement')]:
            self.user.user_permissions.add(Permission.objects.get(content_type__app_label=app, codename=codename))
        self.client.force_login(self.user)
        self.data = {
            'category': self.category.pk, 'reference': 'S1', 'name': 'Sensor nuevo',
            'initial_quantity': 10, 'minimum_quantity': 2, 'maximum_quantity': 50,
        }

    def test_single_submission_creates_component_stock_and_initial_movement(self):
        response = self.client.post(reverse('component_create'), self.data)
        self.assertRedirects(response, reverse('component_search'))
        component = Component.objects.get(reference='S1')
        self.assertEqual(component.stock.quantity, 10)
        movement = component.stock.movements.get()
        self.assertEqual(movement.quantity, 10)
        self.assertEqual(movement.movement_type, StockMovement.ENTRY)
        self.assertContains(self.client.get(reverse('component_search')), 'Sensor nuevo')

    def test_zero_initial_quantity_has_stock_without_zero_movement(self):
        self.data['initial_quantity'] = 0
        self.client.post(reverse('component_create'), self.data)
        self.assertEqual(Stock.objects.get().quantity, 0)
        self.assertFalse(StockMovement.objects.exists())

    def test_invalid_quantities_do_not_create_partial_records(self):
        for changes in [{'initial_quantity': -1}, {'maximum_quantity': 5}, {'minimum_quantity': 51}]:
            with self.subTest(changes=changes):
                response = self.client.post(reverse('component_create'), {**self.data, **changes})
                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.context['form'].errors)
                self.assertFalse(Component.objects.exists())
                self.assertFalse(Stock.objects.exists())

    def test_duplicate_submission_does_not_double_stock(self):
        self.client.post(reverse('component_create'), self.data)
        response = self.client.post(reverse('component_create'), self.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        self.assertEqual(Component.objects.count(), 1)
        self.assertEqual(Stock.objects.get().quantity, 10)
        self.assertEqual(StockMovement.objects.count(), 1)

    def test_save_and_add_another_redirects_to_empty_form(self):
        response = self.client.post(reverse('component_create'), {**self.data, 'save_another': '1'})
        self.assertRedirects(response, reverse('component_create'))
        self.assertFalse(self.client.get(reverse('component_create')).context['form'].is_bound)

    def test_nonstaff_user_with_permissions_can_use_quick_create(self):
        response = self.client.get(reverse('component_create'))
        self.assertContains(response, 'Nuevo componente')
        self.assertContains(response, __version__)

    def test_anonymous_redirects_to_login_and_user_without_permission_gets_403(self):
        self.client.logout()
        response = self.client.get(reverse('component_create'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('login')))
        viewer = get_user_model().objects.create_user('viewer')
        self.client.force_login(viewer)
        self.assertEqual(self.client.post(reverse('component_create'), self.data).status_code, 403)
        self.assertFalse(Component.objects.exists())

    def test_csrf_is_required(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.user)
        self.assertEqual(client.post(reverse('component_create'), self.data).status_code, 403)
        self.assertFalse(Component.objects.exists())

    def test_login_and_logout_use_local_navigation(self):
        self.client.logout()
        self.assertContains(self.client.get(reverse('login')), 'Iniciar sesión')
        response = self.client.post(reverse('login'), {'username': 'operator', 'password': 'test-only'})
        self.assertRedirects(response, reverse('component_search'))
        self.assertRedirects(self.client.post(reverse('logout')), reverse('login'))

    def test_service_rolls_back_component_when_stock_validation_fails(self):
        from apps.components.services import create_component_with_stock
        component = Component(category=self.category, reference='S1', name='Sensor')
        with self.assertRaises(ValidationError):
            create_component_with_stock(component, initial_quantity=10, maximum_quantity=5)
        self.assertFalse(Component.objects.exists())
        self.assertFalse(Stock.objects.exists())
