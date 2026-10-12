from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class ProfileTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user('diego', password='test-only')
        self.other = get_user_model().objects.create_user('other', first_name='Otra cuenta')
        self.client.force_login(self.user)

    def test_edit_own_profile_ignores_identity_and_privilege_injection(self):
        response = self.client.post(reverse('profile_edit'), {
            'first_name': 'Diego', 'last_name': 'Gómez', 'email': 'diego@example.test',
            'pk': self.other.pk, 'username': 'intruso', 'is_superuser': 'on', 'is_staff': 'on',
        })
        self.assertRedirects(response, reverse('profile_edit'))
        self.user.refresh_from_db()
        self.other.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Diego')
        self.assertEqual(self.user.username, 'diego')
        self.assertFalse(self.user.is_superuser)
        self.assertFalse(self.user.is_staff)
        self.assertEqual(self.other.first_name, 'Otra cuenta')
        self.assertTrue(self.user.check_password('test-only'))
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.pk)

    def test_invalid_email_preserves_fields_without_save(self):
        response = self.client.post(reverse('profile_edit'), {'first_name': 'Nuevo', 'email': 'invalid'})
        self.assertContains(response, 'Nuevo')
        self.assertTrue(response.context['form'].errors)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, '')

    def test_profile_requires_session_and_csrf(self):
        self.client.logout()
        self.assertEqual(self.client.get(reverse('profile_edit')).status_code, 302)
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.user)
        self.assertEqual(client.post(reverse('profile_edit'), {'first_name': 'Cambio'}).status_code, 403)
