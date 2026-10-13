from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from apps.components.models import Category, Component
from .pdf_catalog import build_catalog_pdf


class CatalogPDFTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user('lector_pdf')
        self.user.user_permissions.add(Permission.objects.get(codename='view_component'))
        self.client.force_login(self.user)
        category = Category.objects.create(name='Resistencias', slug='resistencias')
        self.components = [Component.objects.create(category=category, reference=f'R-{i:02}',
                           name=f'Resistencia {i:02}', value='10 kΩ') for i in range(28)]
        Component.objects.create(category=category, reference='INACTIVO', name='Oculto', is_active=False)

    def test_download_exports_all_matching_pages_and_protected_headers(self):
        with patch('apps.core.pdf_catalog.build_catalog_pdf', wraps=build_catalog_pdf) as build:
            response = self.client.get(reverse('component_export_pdf'), {'q': 'Resistencia', 'page': '2'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content.startswith(b'%PDF-'))
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn('attachment;', response['Content-Disposition'])
        self.assertEqual(response['Cache-Control'], 'private, no-store')
        rows, filters = build.call_args.args
        self.assertEqual([row.pk for row in rows], [row.pk for row in self.components])
        self.assertEqual(filters['q'], 'Resistencia')
        self.assertEqual(self.client.get(reverse('component_search')).context['page_obj'].paginator.count, 28)

    def test_filters_and_empty_export_are_valid(self):
        with patch('apps.core.pdf_catalog.build_catalog_pdf', wraps=build_catalog_pdf) as build:
            response = self.client.get(reverse('component_export_pdf'), {'q': 'R-27', 'availability': 'empty'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual([row.reference for row in build.call_args.args[0]], ['R-27'])
        with patch('apps.core.pdf_catalog.build_catalog_pdf', wraps=build_catalog_pdf) as build:
            response = self.client.get(reverse('component_export_pdf'), {'q': 'sin-resultados'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(build.call_args.args[0], [])
        self.assertTrue(response.content.startswith(b'%PDF-'))

    def test_export_requires_session_and_inventory_permission(self):
        self.client.logout()
        self.assertEqual(self.client.get(reverse('component_export_pdf')).status_code, 302)
        self.client.force_login(get_user_model().objects.create_user('sin_permiso'))
        self.assertEqual(self.client.get(reverse('component_export_pdf')).status_code, 403)
