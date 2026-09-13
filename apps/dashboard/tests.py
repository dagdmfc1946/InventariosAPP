from decimal import Decimal

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from apps.components.models import Category, Component
from apps.documents.models import Datasheet
from apps.inventory.models import Stock, StockMovement
from apps.suppliers.models import Supplier, SupplierOffer


class DashboardViewTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name='Sensores', slug='sensores')
        self.component_low = Component.objects.create(
            category=category,
            reference='S1',
            name='Sensor LM35',
            value='3V',
        )
        self.component_no_datasheet = Component.objects.create(
            category=category,
            reference='S2',
            name='Sensor DHT22',
            value='5V',
        )
        self.component_no_price = Component.objects.create(
            category=category,
            reference='S3',
            name='Sensor TMP36',
            value='5V',
        )
        self.component_with_datasheet = Component.objects.create(
            category=category,
            reference='S4',
            name='Sensor BMP280',
            value='3.3V',
        )

        Stock.objects.create(component=self.component_low, quantity=5, minimum_quantity=5, maximum_quantity=20)
        Stock.objects.create(component=self.component_no_datasheet, quantity=12, minimum_quantity=2, maximum_quantity=50)
        Stock.objects.create(component=self.component_no_price, quantity=0, minimum_quantity=1, maximum_quantity=30)
        Stock.objects.create(component=self.component_with_datasheet, quantity=8, minimum_quantity=2, maximum_quantity=30)

        Datasheet.objects.create(
            component=self.component_with_datasheet,
            file=SimpleUploadedFile('bmp280.pdf', b'%PDF-1.4\n', content_type='application/pdf'),
        )

        supplier = Supplier.objects.create(name='Distribuidor Test')
        SupplierOffer.objects.create(
            component=self.component_low,
            supplier=supplier,
            part_number='LM35-01',
            price=Decimal('1.25'),
            currency='EUR',
        )

        StockMovement.objects.create(
            stock=Stock.objects.get(component=self.component_low),
            movement_type=StockMovement.EXIT,
            quantity=2,
            reason='Salida de prueba',
        )

    def test_dashboard_shows_key_metrics(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['low_stock_count'], 2)
        self.assertEqual(response.context['missing_datasheets_count'], 3)
        self.assertEqual(response.context['missing_prices_count'], 3)
        self.assertEqual(len(response.context['recent_movements']), 1)
