from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class ProfileTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user('diego', password='test-only')
        self.other = get_user_model().objects.create_user('other', first_name='Otra cuenta')
        self.client.force_login(self.user)

    def test_rename_own_profile_ignores_other_account_and_privilege_injection(self):
        response = self.client.post(reverse('profile_edit'), {
            'first_name': 'Diego', 'last_name': 'GÃ³mez', 'email': 'diego@example.test',
            'pk': self.other.pk, 'username': 'intruso', 'is_superuser': 'on', 'is_staff': 'on',
        })
        self.assertRedirects(response, reverse('profile_edit'))
        self.user.refresh_from_db()
        self.other.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Diego')
        self.assertEqual(self.user.username, 'intruso')
        self.assertFalse(self.user.is_superuser)
        self.assertFalse(self.user.is_staff)
        self.assertEqual(self.other.first_name, 'Otra cuenta')
        self.assertTrue(self.user.check_password('test-only'))
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.pk)

    def test_invalid_email_preserves_fields_without_save(self):
        response = self.client.post(reverse('profile_edit'), {'username': 'diego', 'first_name': 'Nuevo', 'email': 'invalid'})
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

    def test_username_change_keeps_session_and_new_login(self):
        response = self.client.post(reverse('profile_edit'), {
            'username': 'diego.nuevo', 'first_name': 'Diego', 'last_name': '', 'email': '',
        })
        self.assertRedirects(response, reverse('profile_edit'))
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.pk)
        self.assertContains(self.client.get(reverse('profile_edit')), 'diego.nuevo')
        self.client.logout()
        self.assertFalse(self.client.login(username='diego', password='test-only'))
        self.assertTrue(self.client.login(username='diego.nuevo', password='test-only'))

    def test_duplicate_invalid_and_empty_usernames_do_not_save(self):
        for username in ('other', 'OTHER', 'nombre con espacios', ''):
            with self.subTest(username=username):
                response = self.client.post(reverse('profile_edit'), {
                    'username': username, 'first_name': 'No guardar', 'email': '',
                })
                self.assertEqual(response.status_code, 200)
                self.assertIn('username', response.context['form'].errors)
                self.user.refresh_from_db()
                self.assertEqual(self.user.username, 'diego')
                self.assertEqual(self.user.first_name, '')
