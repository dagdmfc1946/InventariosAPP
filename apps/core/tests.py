import shutil
import tempfile
from pathlib import Path

from django.test import TestCase
from django.urls import reverse

from apps.components.models import Category, Component
from apps.inventory.models import Stock
from backups.backup_local import backup_project, restore_backup


class BackupLocalScriptTests(TestCase):
    def test_backup_and_restore_project_files(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            backup_root = root / 'backups_out'
            db_path = root / 'db.sqlite3'
            media_dir = root / 'media' / 'datasheets'
            media_dir.mkdir(parents=True)
            db_path.write_bytes(b'data')
            (media_dir / 'sample.pdf').write_bytes(b'pdf-content')

            backup_dir = backup_project(project_root=root, output_dir=backup_root)
            self.assertTrue((backup_dir / 'db.sqlite3').exists())
            self.assertTrue((backup_dir / 'media' / 'datasheets' / 'sample.pdf').exists())

            db_path.unlink()
            shutil.rmtree(media_dir.parent)

            restored = restore_backup(backup_dir, project_root=root)
            self.assertTrue((restored / 'db.sqlite3').exists())
            self.assertTrue((restored / 'media' / 'datasheets' / 'sample.pdf').exists())


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

    def test_site_home_redirects_to_search(self):
        response = self.client.get('/')
        self.assertRedirects(response, reverse('component_search'))

    def test_search_orders_by_stock_desc(self):
        response = self.client.get(reverse('component_search'), {'q': 'sensor', 'ordering': '-stock'})
        self.assertEqual(response.status_code, 200)
        results = list(response.context['components'])
        self.assertEqual(results[0].reference, 'S1')
        self.assertEqual(results[1].reference, 'S2')

    def test_search_excludes_inactive_components(self):
        self.sensor_dht22.is_active = False
        self.sensor_dht22.save(update_fields=['is_active'])
        response = self.client.get(reverse('component_search'), {'q': 'sensor'})
        self.assertNotContains(response, 'Sensor humedad DHT22')
