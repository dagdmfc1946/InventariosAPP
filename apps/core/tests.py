from django.test import TestCase
from django.urls import reverse

from apps.components.models import Category, Component
from apps.inventory.models import Stock


class ComponentSearchViewTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name='Sensores', slug='sensores')
        self.sensor_lm35 = Component.objects.create(
            category=category,
            reference='S1',
            name='Sensor temperatura LM35',
            value='3V',
        )
        self.sensor_dht22 = Component.objects.create(
            category=category,
            reference='S2',
            name='Sensor humedad DHT22',
            value='5V',
        )
        Stock.objects.create(component=self.sensor_lm35, quantity=10, minimum_quantity=2, maximum_quantity=50)
        Stock.objects.create(component=self.sensor_dht22, quantity=3, minimum_quantity=1, maximum_quantity=30)

    def test_search_filters_by_text(self):
        response = self.client.get(reverse('component_search'), {'q': 'sensor'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sensor temperatura LM35')
        self.assertContains(response, 'Sensor humedad DHT22')

    def test_search_orders_by_stock_desc(self):
        response = self.client.get(reverse('component_search'), {'q': 'sensor', 'ordering': '-stock'})
        self.assertEqual(response.status_code, 200)
        results = list(response.context['components'])
        self.assertEqual(results[0].reference, 'S1')
        self.assertEqual(results[1].reference, 'S2')
