from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.components.models import Category, Component
from apps.inventory.models import Stock, StockMovement


class StockMovementValidationTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name='Sensores', slug='sensores')
        component = Component.objects.create(
            category=category,
            reference='S1',
            name='Sensor de temperatura',
            value='LM35',
        )
        self.stock = Stock.objects.create(
            component=component,
            quantity=10,
            minimum_quantity=2,
            maximum_quantity=50,
        )

    def test_entry_increases_quantity(self):
        movement = StockMovement.objects.create(
            stock=self.stock,
            movement_type=StockMovement.ENTRY,
            quantity=5,
            reason='Compra inicial',
        )
        movement.full_clean()
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.quantity, 15)

    def test_exit_reduces_quantity_and_rejects_negative(self):
        movement = StockMovement(
            stock=self.stock,
            movement_type=StockMovement.EXIT,
            quantity=20,
            reason='Uso en montaje',
        )
        with self.assertRaises(ValidationError):
            movement.full_clean()

    def test_adjustment_allows_value_change(self):
        movement = StockMovement(
            stock=self.stock,
            movement_type=StockMovement.ADJUSTMENT,
            quantity=-3,
            reason='Ajuste por inventario',
        )
        movement.full_clean()
        movement.save()
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.quantity, 7)
