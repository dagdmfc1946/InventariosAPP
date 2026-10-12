import tempfile
from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError, OperationalError
from django.test import TestCase, override_settings
from django.urls import reverse
from pathlib import Path
from apps.components.models import Category, Component
from apps.core.roles import configure_inventory_roles
from .models import Datasheet


class ProtectedFileTests(TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        settings = override_settings(MEDIA_ROOT=self.directory.name)
        settings.enable()
        self.addCleanup(settings.disable)
        self.user = get_user_model().objects.create_user('operator')
        self.user.groups.add(configure_inventory_roles()['operator'])
        self.client.force_login(self.user)
        self.component = Component.objects.create(category=Category.objects.create(name='Sensors'), reference='1', name='Sensor')

    def upload(self, content=b'%PDF-1.4\n'):
        return self.client.post(reverse('datasheet_upload', args=[self.component.pk]), {
            'file': SimpleUploadedFile('manual.pdf', content, content_type='application/pdf'),
        })

    def test_upload_download_and_raw_media_require_authorization(self):
        self.assertRedirects(self.upload(), reverse('component_detail', args=[self.component.pk]))
        sheet = Datasheet.objects.get()
        url = reverse('datasheet_download', args=[sheet.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(b''.join(response.streaming_content), b'%PDF-1.4\n')
        response.close()
        response = self.client.get(sheet.file.url)
        self.assertEqual(response.status_code, 200)
        response.close()
        self.client.logout()
        self.assertEqual(self.client.get(url).status_code, 302)
        self.assertEqual(self.client.get(sheet.file.url).status_code, 302)
        self.client.force_login(get_user_model().objects.create_user('no_permissions'))
        self.assertEqual(self.client.get(url).status_code, 403)
        self.assertEqual(self.client.get(sheet.file.url).status_code, 403)

    def test_disguised_pdf_rejected_without_orphans(self):
        self.upload(b'<html>Not a PDF</html>')
        self.assertFalse(Datasheet.objects.exists())
        self.assertEqual(list(Path(self.directory.name).rglob('*.pdf')), [])

    def test_database_failure_removes_file_written_before_insert(self):
        # FileField escribe el fichero antes de INSERT: simular fallo justo después.
        for error in (IntegrityError('test-only'), OperationalError('database is locked')):
            with self.subTest(error=type(error).__name__):
                with patch.object(Datasheet, '_save_table', side_effect=error):
                    response = self.upload()
                self.assertEqual(response.status_code, 302)
                self.assertFalse(Datasheet.objects.exists())
                self.assertEqual(list(Path(self.directory.name).rglob('*.pdf')), [])

    def test_missing_file_and_unregistered_path_return_404(self):
        sheet = Datasheet.objects.create(component=self.component, file='datasheets/missing.pdf')
        response = self.client.get(reverse('datasheet_download', args=[sheet.pk]))
        self.assertContains(response, 'Vuelve a adjuntar', status_code=404)
        self.assertEqual(self.client.get('/media/not_registered.pdf').status_code, 404)
