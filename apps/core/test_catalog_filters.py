from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from apps.components.models import Category, Component
from apps.inventory.models import Stock


class CatalogFilterTests(TestCase):
    def setUp(self):
        self.client.force_login(get_user_model().objects.create_superuser('catalogo', password='Test-7418!'))
        self.category = Category.objects.create(name='Sensores')
        for index in range(27):
            item = Component.objects.create(category=self.category, name=f'Sensor {index:02}', reference=f'S{index}')
            Stock.objects.create(component=item, quantity=index, minimum_quantity=1)

    def test_combined_filters_and_pagination_preserve_query(self):
        response = self.client.get(reverse('component_search'), {'q': 'Sensor', 'category': self.category.pk, 'attention': 'no_pdf', 'ordering': '-stock'})
        self.assertEqual(len(response.context['components']), 25)
        self.assertEqual(response.context['page_obj'].paginator.count, 27)
        self.assertContains(response, 'attention=no_pdf')
        response = self.client.get(reverse('component_search'), {'category': self.category.pk, 'availability': 'available', 'attention': 'low'})
        self.assertEqual([item.reference for item in response.context['components']], ['S1'])

    def test_invalid_page_and_category_are_safe_and_order_is_stable(self):
        for page in ('abc', '-4', '999'):
            response = self.client.get(reverse('component_search'), {'page': page, 'category': 'bad', 'ordering': 'invalid'})
            self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('component_search'), {'availability': 'empty'})
        self.assertEqual([item.reference for item in response.context['components']], ['S0'])

    def test_dashboard_links_to_matching_catalog_filters(self):
        response = self.client.get(reverse('dashboard'))
        for key in ('low', 'no_pdf', 'no_offer'):
            self.assertContains(response, f'?attention={key}')
