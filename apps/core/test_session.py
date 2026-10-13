from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class SharedSessionTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser('responsable', password='Anterior-8174!')
        self.client.force_login(self.user)

    def test_shared_actions_render_on_application_and_admin(self):
        for route in ('component_search', 'dashboard', 'profile_edit', 'admin:index', 'password_change'):
            with self.subTest(route=route):
                response = self.client.get(reverse(route))
                for text in ('Sesión activa', 'Mi perfil', 'Cambiar contraseña', 'Salir', 'css/session.css'):
                    self.assertContains(response, text)
                self.assertContains(response, reverse('password_change'))

    def test_normal_user_changes_own_password_without_losing_session(self):
        self.user.is_staff = self.user.is_superuser = False
        self.user.save()
        response = self.client.post(reverse('password_change'), {
            'old_password': 'Anterior-8174!', 'new_password1': 'Nueva-clave-7364!',
            'new_password2': 'Nueva-clave-7364!',
        })
        self.assertRedirects(response, reverse('password_change_done'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('Nueva-clave-7364!'))
        self.assertEqual(self.client.session['_auth_user_id'], str(self.user.pk))
