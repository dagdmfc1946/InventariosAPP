from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from time import sleep
from unittest.mock import patch

from django.db import IntegrityError, OperationalError, close_old_connections, models, transaction
from django.db.models.deletion import ProtectedError
from django.test import RequestFactory, TestCase, TransactionTestCase

from apps.components.models import Category, Component
from apps.inventory.admin import StockAdmin, StockMovementAdmin
from apps.inventory.models import Stock, StockMovement


class StockIntegrityTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Integridad')
        self.stock = self.make_stock('INT-1')

    def make_stock(self, reference):
        component = Component.objects.create(
            category=self.category, reference=reference, name=reference,
        )
        return Stock.objects.create(
            component=component, quantity=10,
            minimum_quantity=2, maximum_quantity=50,
        )

    def make_movement(self, **changes):
        values = {
            'stock': self.stock, 'movement_type': StockMovement.ENTRY,
            'quantity': 3, 'reason': 'Recepción',
        }
        values.update(changes)
        return StockMovement.objects.create(**values)

    def test_resaving_existing_movement_does_not_apply_it_twice(self):
        movement = self.make_movement()
        movement.save()
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.quantity, 13)
        self.assertEqual(StockMovement.objects.count(), 1)

    def test_existing_movement_fields_are_immutable(self):
        movement = self.make_movement()
        other_stock = self.make_stock('INT-2')
        changes = {
            'quantity': 4, 'movement_type': StockMovement.EXIT,
            'stock': other_stock, 'reason': 'Motivo modificado',
        }
        for field, value in changes.items():
            with self.subTest(field=field):
                candidate = StockMovement.objects.get(pk=movement.pk)
                setattr(candidate, field, value)
                with self.assertRaises(ValidationError):
                    candidate.save()
        movement.refresh_from_db()
        self.stock.refresh_from_db()
        other_stock.refresh_from_db()
        self.assertEqual(movement.quantity, 3)
        self.assertEqual(movement.movement_type, StockMovement.ENTRY)
        self.assertEqual(movement.stock_id, self.stock.pk)
        self.assertEqual(movement.reason, 'Recepción')
        self.assertEqual(self.stock.quantity, 13)
        self.assertEqual(other_stock.quantity, 10)

    def test_individual_movement_deletion_is_blocked(self):
        movement = self.make_movement()
        with self.assertRaises(ValidationError):
            movement.delete()
        self.assertTrue(StockMovement.objects.filter(pk=movement.pk).exists())

    def test_queryset_movement_deletion_is_blocked(self):
        movement = self.make_movement()
        with self.assertRaises(ValidationError):
            StockMovement.objects.filter(pk=movement.pk).delete()
        self.assertTrue(StockMovement.objects.filter(pk=movement.pk).exists())

    def test_external_transaction_rolls_back_balance_and_movement(self):
        for kind, quantity in (
            (StockMovement.ENTRY, 3), (StockMovement.EXIT, 3),
            (StockMovement.ADJUSTMENT, -3),
        ):
            with self.subTest(movement_type=kind):
                with self.assertRaises(RuntimeError):
                    with transaction.atomic():
                        self.make_movement(movement_type=kind, quantity=quantity)
                        raise RuntimeError('Cancelar operación completa')
                self.stock.refresh_from_db()
                self.assertEqual(self.stock.quantity, 10)
                self.assertEqual(StockMovement.objects.count(), 0)

    def test_cached_stock_instances_do_not_lose_updates(self):
        first = Stock.objects.get(pk=self.stock.pk)
        second = Stock.objects.get(pk=self.stock.pk)
        self.make_movement(stock=first, quantity=3)
        self.make_movement(stock=second, quantity=4)
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.quantity, 17)
        self.assertEqual(StockMovement.objects.count(), 2)

    def test_cached_stock_cannot_allow_exit_using_old_balance(self):
        first = Stock.objects.get(pk=self.stock.pk)
        second = Stock.objects.get(pk=self.stock.pk)
        self.make_movement(stock=first, movement_type=StockMovement.EXIT, quantity=8)
        with self.assertRaises(ValidationError):
            self.make_movement(stock=second, movement_type=StockMovement.EXIT, quantity=5)
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.quantity, 2)
        self.assertEqual(StockMovement.objects.count(), 1)

    def test_minimum_cannot_exceed_configured_maximum(self):
        self.stock.minimum_quantity = 51
        with self.assertRaises(ValidationError):
            self.stock.full_clean()

    def test_failed_movement_insert_rolls_back_balance(self):
        movement = StockMovement(stock=self.stock, quantity=3)
        # Fallar exactamente al insertar el historial, después de actualizar el saldo.
        with patch.object(models.Model, 'save', side_effect=IntegrityError('Inserción fallida')):
            with self.assertRaises(IntegrityError):
                movement.save()
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.quantity, 10)
        self.assertEqual(StockMovement.objects.count(), 0)
        self.assertIsNone(movement.pk)
        self.assertTrue(movement._state.adding)
        movement.save()
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.quantity, 13)
        self.assertEqual(StockMovement.objects.count(), 1)

    def test_component_with_inventory_history_cannot_be_deleted(self):
        movement = self.make_movement()
        with self.assertRaises(ProtectedError):
            self.stock.component.delete()
        self.assertTrue(Stock.objects.filter(pk=self.stock.pk).exists())
        self.assertTrue(StockMovement.objects.filter(pk=movement.pk).exists())

    def test_direct_stock_balance_edit_is_rejected(self):
        self.stock.quantity = 100
        with self.assertRaises(ValidationError):
            self.stock.save()
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.quantity, 10)

    def test_lowering_maximum_below_balance_is_rejected_on_save(self):
        self.stock.maximum_quantity = 5
        with self.assertRaises(ValidationError):
            self.stock.save()
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.maximum_quantity, 50)

    def test_queryset_movement_update_is_rejected(self):
        movement = self.make_movement()
        with self.assertRaises(ValidationError):
            StockMovement.objects.filter(pk=movement.pk).update(quantity=4)
        movement.refresh_from_db()
        self.assertEqual(movement.quantity, 3)

    def test_bulk_movement_creation_is_rejected(self):
        with self.assertRaises(ValidationError):
            StockMovement.objects.bulk_create([
                StockMovement(stock=self.stock, quantity=3),
            ])
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.quantity, 10)
        self.assertEqual(StockMovement.objects.count(), 0)

    def test_exact_maximum_and_existing_movement_validation(self):
        movement = self.make_movement(quantity=40)
        movement.full_clean()
        movement.save()
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.quantity, 50)
        self.assertEqual(StockMovement.objects.count(), 1)
        with self.assertRaises(ValidationError):
            self.make_movement(quantity=1)

    def test_exit_can_reach_zero_and_existing_validation_does_not_repeat_it(self):
        movement = self.make_movement(movement_type=StockMovement.EXIT, quantity=10)
        movement.full_clean()
        movement.save()
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.quantity, 0)
        self.assertEqual(StockMovement.objects.count(), 1)


class InventoryAdminIntegrityTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name='Administración')
        component = Component.objects.create(
            category=category, reference='ADMIN-1', name='Prueba administrativa',
        )
        self.stock = Stock.objects.create(component=component, quantity=10)
        self.movement = StockMovement.objects.create(stock=self.stock, quantity=3)
        self.request = RequestFactory().get('/admin/')
        self.request.user = get_user_model().objects.create_superuser(
            username='integrity-admin', email='admin@example.test', password='test-only',
        )

    def test_existing_stock_quantity_is_readonly(self):
        model_admin = StockAdmin(Stock, admin.site)
        self.assertIn('quantity', model_admin.get_readonly_fields(self.request, self.stock))

    def test_stock_with_history_cannot_be_deleted(self):
        model_admin = StockAdmin(Stock, admin.site)
        self.assertFalse(model_admin.has_delete_permission(self.request, self.stock))

    def test_existing_movement_cannot_be_changed_or_deleted(self):
        model_admin = StockMovementAdmin(StockMovement, admin.site)
        self.assertFalse(model_admin.has_change_permission(self.request, self.movement))
        self.assertFalse(model_admin.has_delete_permission(self.request, self.movement))


class ConcurrentStockIntegrityTests(TransactionTestCase):
    def test_two_competing_exits_cannot_overspend_stock(self):
        category = Category.objects.create(name='Concurrencia')
        component = Component.objects.create(category=category, reference='CON-1', name='Concurrente')
        stock = Stock.objects.create(component=component, quantity=10)
        start = Barrier(2)

        def try_exit():
            close_old_connections()
            try:
                start.wait(timeout=5)
                # SQLite puede rechazar la escritura mientras otro hilo mantiene el bloqueo.
                # Reintentar aquí permite comprobar el saldo sin prometer ausencia de bloqueos.
                for attempt in range(5):
                    try:
                        StockMovement.objects.create(
                            stock_id=stock.pk, movement_type=StockMovement.EXIT, quantity=7,
                        )
                        return 'saved'
                    except ValidationError:
                        return 'rejected'
                    except OperationalError as error:
                        if 'locked' not in str(error).lower():
                            raise
                        if attempt == 4:
                            return 'locked'
                        sleep(0.02 * (attempt + 1))
            finally:
                close_old_connections()

        with ThreadPoolExecutor(max_workers=2) as executor:
            outcomes = list(executor.map(lambda _: try_exit(), range(2)))
        stock.refresh_from_db()
        self.assertEqual(outcomes.count('saved'), 1)
        self.assertGreaterEqual(stock.quantity, 0)
        self.assertLessEqual(stock.quantity, 10)
        movements = StockMovement.objects.filter(stock=stock)
        self.assertEqual(movements.count(), 1)
        self.assertEqual(stock.quantity, 10 - sum(movements.values_list('quantity', flat=True)))
