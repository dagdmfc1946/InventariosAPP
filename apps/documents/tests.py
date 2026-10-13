from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from apps.components.models import Category, Component
from apps.documents.models import Datasheet


class DatasheetValidationTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Microcontroladores', slug='microcontroladores')
        self.component = Component.objects.create(
            category=self.category,
            reference='U1',
            name='ESP32-WROOM-32',
            value='WiFi + BT',
        )

    def test_accepts_valid_pdf(self):
        file = SimpleUploadedFile('esp32.pdf', b'%PDF-1.4\n', content_type='application/pdf')
        datasheet = Datasheet(component=self.component, file=file)
        datasheet.full_clean()

    def test_rejects_non_pdf(self):
        file = SimpleUploadedFile('esp32.txt', b'not a pdf', content_type='text/plain')
        datasheet = Datasheet(component=self.component, file=file)
        with self.assertRaises(ValidationError):
            datasheet.full_clean()

    def test_rejects_files_over_20mb(self):
        file = SimpleUploadedFile('large.pdf', b'a' * (21 * 1024 * 1024), content_type='application/pdf')
        datasheet = Datasheet(component=self.component, file=file)
        with self.assertRaises(ValidationError):
            datasheet.full_clean()
