from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse


class AdminInterfaceTests(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser('responsable', password='Test-review-6842!')
        self.client.force_login(self.admin)

    def test_admin_has_shared_navigation_and_spanish_sections(self):
        response = self.client.get(reverse('admin:index'))
        self.assertContains(response, 'css/admin.css')
        for text in ('InventariosAPP', 'Componentes', 'Resumen', 'Ubicaciones', 'Fichas técnicas', 'Proveedores'):
            self.assertContains(response, text)

    def test_create_normal_user_password_and_application_login(self):
        response = self.client.post(reverse('admin:auth_user_add'), {
            'role': 'reader', 'username': 'operador', 'password1': 'Local-test-9876!',
            'password2': 'Local-test-9876!', 'usable_password': 'true',
            'is_staff': 'on', 'is_superuser': 'on', '_save': 'Guardar',
        })
        self.assertEqual(response.status_code, 302)
        account = get_user_model().objects.get(username='operador')
        self.assertTrue(account.check_password('Local-test-9876!'))
        self.assertFalse(account.is_staff)
        self.assertFalse(account.is_superuser)
        self.client.logout()
        response = self.client.post(reverse('login'), {'username': 'operador', 'password': 'Local-test-9876!'})
        self.assertRedirects(response, reverse('component_search'))
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 302)

    def test_user_form_cannot_promote_to_administrator(self):
        account = get_user_model().objects.create_user('lector', password='Local-test-9876!')
        response = self.client.get(reverse('admin:auth_user_change', args=[account.pk]))
        self.assertNotContains(response, 'name="is_superuser"')
        self.assertNotContains(response, 'name="is_staff"')
        response = self.client.post(reverse('admin:auth_user_change', args=[account.pk]), {
            'username': account.username, 'is_active': 'on', 'is_superuser': 'on',
            'is_staff': 'on', '_save': 'Guardar',
        })
        self.assertEqual(response.status_code, 302)
        account.refresh_from_db()
        self.assertFalse(account.is_superuser)
        self.assertFalse(account.is_staff)
        self.assertTrue(account.check_password('Local-test-9876!'))

    def test_admin_login_explains_normal_account_route(self):
        self.client.logout()
        response = self.client.get(reverse('admin:login'))
        self.assertContains(response, reverse('login'))
        self.assertContains(response, 'usuarios del aplicativo')

    def test_permissions_have_spanish_labels_without_rewriting_stored_names(self):
        account = get_user_model().objects.create_user('lector')
        response = self.client.get(reverse('admin:auth_user_change', args=[account.pk]))
        self.assertContains(response, 'Puede agregar')
        self.assertNotContains(response, 'Can add')

    def test_staff_with_user_permissions_cannot_manage_accounts(self):
        account = get_user_model().objects.create_user('auxiliar', is_staff=True)
        account.user_permissions.add(*Permission.objects.filter(content_type__app_label='auth', content_type__model='user'))
        self.client.force_login(account)
        self.assertEqual(self.client.get(reverse('admin:auth_user_add')).status_code, 403)
        self.assertEqual(self.client.get(reverse('admin:auth_user_change', args=[self.admin.pk])).status_code, 403)

    def test_inactive_normal_account_cannot_login(self):
        get_user_model().objects.create_user('inactivo', password='Local-test-9876!', is_active=False)
        self.client.logout()
        response = self.client.post(reverse('login'), {'username': 'inactivo', 'password': 'Local-test-9876!'})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_superuser_creation_in_terminal_remains_available(self):
        account = get_user_model().objects.create_superuser('otro_admin', password='Local-test-9876!')
        self.assertTrue(account.is_superuser)
        self.assertTrue(account.is_staff)
        self.assertEqual(self.client.get(reverse('admin:auth_user_delete', args=[account.pk])).status_code, 403)

    def test_password_status_hides_hash_details_and_preserves_password(self):
        account = get_user_model().objects.create_user('sin_detalles', password='Local-test-9876!')
        original_hash = account.password
        response = self.client.get(reverse('admin:auth_user_change', args=[account.pk]))
        self.assertContains(response, 'Contraseña configurada.')
        self.assertContains(response, 'href="../password/"')
        for secret in (original_hash, 'pbkdf2_sha256', 'algoritmo:', 'iteraciones:', 'función resumen:'):
            self.assertNotContains(response, secret)
        response = self.client.post(reverse('admin:auth_user_change', args=[account.pk]), {
            'username': account.username, 'is_active': 'on', 'password': 'injected', '_save': 'Guardar',
        })
        self.assertEqual(response.status_code, 302)
        account.refresh_from_db()
        self.assertEqual(account.password, original_hash)

    def test_password_status_for_account_without_password(self):
        account = get_user_model().objects.create_user('sin_clave')
        response = self.client.get(reverse('admin:auth_user_change', args=[account.pk]))
        self.assertContains(response, 'Sin contraseña para iniciar sesión.')
        self.assertContains(response, 'Establecer contraseña')
