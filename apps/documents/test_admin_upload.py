import tempfile

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from apps.components.models import Category, Component
from .models import Datasheet


class DatasheetAdminUploadTests(TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        settings = override_settings(MEDIA_ROOT=directory.name)
        settings.enable()
        self.addCleanup(settings.disable)
        self.client.force_login(get_user_model().objects.create_superuser('responsable', password='Local-test-9876!'))
        category = Category.objects.create(name='Sensors')
        self.component = Component.objects.create(category=category, reference='A1', name='English name')

    def test_save_and_continue_then_save_without_new_file(self):
        response = self.client.post(reverse('admin:documents_datasheet_add'), {
            'component': self.component.pk,
            'file': SimpleUploadedFile('manual.pdf', b'%PDF-1.4\n'), '_continue': 'Guardar',
        })
        sheet = Datasheet.objects.get()
        change_url = reverse('admin:documents_datasheet_change', args=[sheet.pk])
        self.assertRedirects(response, change_url)
        filename = sheet.file.name
        response = self.client.post(change_url, {'component': self.component.pk, '_continue': 'Guardar'})
        self.assertRedirects(response, change_url)
        sheet.refresh_from_db()
        self.assertEqual(sheet.file.name, filename)
        self.assertEqual(self.component.name, 'English name')

    def test_missing_existing_pdf_returns_validation_instead_of_server_error(self):
        sheet = Datasheet.objects.create(component=self.component, file='datasheets/missing.pdf')
        response = self.client.post(reverse('admin:documents_datasheet_change', args=[sheet.pk]), {
            'component': self.component.pk, '_continue': 'Guardar',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Vuelva a adjuntar el PDF')

    def test_replacement_recovers_missing_file(self):
        sheet = Datasheet.objects.create(component=self.component, file='datasheets/missing.pdf')
        url = reverse('admin:documents_datasheet_change', args=[sheet.pk])
        response = self.client.post(url, {
            'component': self.component.pk, '_continue': 'Guardar',
            'file': SimpleUploadedFile('replacement.pdf', b'%PDF-1.4\n'),
        })
        self.assertRedirects(response, url)
        sheet.refresh_from_db()
        self.assertTrue(sheet.file.storage.exists(sheet.file.name))
