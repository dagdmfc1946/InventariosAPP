from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.test import TestCase
from django.urls import reverse
from .roles import configure_inventory_roles


class InventoryRolesTests(TestCase):
    def test_role_setup_is_repeatable_without_assigning_existing_accounts(self):
        user = get_user_model().objects.create_user('existing')
        for _ in range(2):
            roles = configure_inventory_roles()
        self.assertEqual(Group.objects.filter(name__startswith='Inventario - ').count(), 2)
        self.assertFalse(user.groups.exists())
        user.groups.add(roles['reader'])
        self.assertTrue(user.has_perm('components.view_component'))
        self.assertFalse(user.has_perm('components.change_component'))
        self.assertFalse(user.is_staff)

    def test_private_catalog_dashboard_and_profile_remain_separate(self):
        for route in ('component_search', 'dashboard'):
            self.assertEqual(self.client.get(reverse(route)).status_code, 302)
        user = get_user_model().objects.create_user('no_role')
        self.client.force_login(user)
        self.assertEqual(self.client.get(reverse('component_search')).status_code, 403)
        self.assertEqual(self.client.get(reverse('dashboard')).status_code, 403)
        self.assertContains(self.client.get(reverse('profile_edit')), 'Mi perfil')

    def test_operator_role_does_not_grant_administration(self):
        user = get_user_model().objects.create_user('operator')
        user.groups.add(configure_inventory_roles()['operator'])
        self.assertTrue(user.has_perm('inventory.change_location'))
        self.assertTrue(user.has_perm('components.change_specification'))
        self.assertFalse(user.has_perm('auth.add_user'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
