from django.contrib.auth import get_user_model
from django.db.models.deletion import ProtectedError
from django.test import TestCase, TransactionTestCase
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.urls import reverse
from apps.components.models import Category, Component
from apps.core.roles import configure_inventory_roles
from .models import Location, Stock
from .services import assign_location_components


class SharedLocationTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name='Sensores')
        self.first = Component.objects.create(category=category, reference='1', name='Uno')
        self.second = Component.objects.create(category=category, reference='2', name='Dos')
        self.location = Location.objects.create(box='Caja 1')

    def test_assign_share_remove_and_protect_location(self):
        assign_location_components(self.location, [self.first, self.second])
        self.assertEqual(self.location.components.count(), 2)
        with self.assertRaises(ProtectedError):
            self.location.delete()
        assign_location_components(self.location, [self.second])
        self.first.refresh_from_db()
        self.assertIsNone(self.first.location)
        self.assertEqual(self.location.components.get(), self.second)

    def test_operator_can_add_components_to_saved_location(self):
        user = get_user_model().objects.create_user('operator')
        user.groups.add(configure_inventory_roles()['operator'])
        self.client.force_login(user)
        response = self.client.post(reverse('location_edit', args=[self.location.pk]), {
            'box': 'Caja 1', 'components': [self.first.pk, self.second.pk],
        })
        self.assertRedirects(response, reverse('location_list'))
        self.assertEqual(self.location.components.count(), 2)

    def test_admin_saved_location_accepts_multiple_components(self):
        user = get_user_model().objects.create_superuser('admin', password='test-only')
        self.client.force_login(user)
        response = self.client.post(reverse('admin:inventory_location_change', args=[self.location.pk]), {
            'box': 'Caja 1', 'components': [self.first.pk, self.second.pk], '_continue': 'Guardar',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.location.components.count(), 2)


class LocationMigrationTests(TransactionTestCase):
    def test_existing_assignments_empty_locations_and_stock_survive(self):
        executor = MigrationExecutor(connection)
        latest = executor.loader.graph.leaf_nodes()
        self.addCleanup(lambda: MigrationExecutor(connection).migrate(latest))
        previous = [('components', '0002_spanish_interface'), ('inventory', '0003_spanish_interface')]
        executor.migrate(previous)
        old = executor.loader.project_state(previous).apps
        category = old.get_model('components', 'Category').objects.create(name='Legacy', slug='legacy')
        component = old.get_model('components', 'Component').objects.create(category=category, reference='OLD', name='Existing English name')
        location = old.get_model('inventory', 'Location').objects.create(component=component, shelf='A')
        empty = old.get_model('inventory', 'Location').objects.create(box='Libre')
        old.get_model('inventory', 'Stock').objects.create(component=component, quantity=17)
        executor = MigrationExecutor(connection)
        executor.migrate(latest)
        upgraded = Component.objects.get(pk=component.pk)
        self.assertEqual(upgraded.location_id, location.pk)
        self.assertEqual(upgraded.stock.quantity, 17)
        self.assertEqual(upgraded.name, 'Existing English name')
        self.assertTrue(Location.objects.filter(pk=empty.pk).exists())
        self.assertEqual(Location.objects.count(), 2)
