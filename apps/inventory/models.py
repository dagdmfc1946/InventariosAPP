from django.core.exceptions import ValidationError
from django.db import models, router, transaction
from django.db.models import F, Q
from django.utils import timezone


class Location(models.Model):
    component = models.OneToOneField('components.Component', on_delete=models.CASCADE, related_name='location', null=True, blank=True)
    shelf = models.CharField(max_length=50, blank=True)
    box = models.CharField(max_length=50, blank=True)
    drawer = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['shelf', 'box', 'drawer']

    def clean(self):
        if not any([self.shelf, self.box, self.drawer, self.description]):
            raise ValidationError('Debe indicar al menos un campo de ubicación.')

    def __str__(self):
        path = [part for part in [self.shelf, self.box, self.drawer] if part]
        if path:
            return ' / '.join(path)
        return self.description or f'Ubicación {self.pk}'


class Stock(models.Model):
    component = models.OneToOneField('components.Component', on_delete=models.CASCADE, related_name='stock')
    quantity = models.PositiveIntegerField(default=0)
    minimum_quantity = models.PositiveIntegerField(default=0)
    maximum_quantity = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['component__reference']

    def clean(self):
        if self.minimum_quantity < 0:
            raise ValidationError({'minimum_quantity': 'No puede ser negativo.'})
        if self.maximum_quantity and self.minimum_quantity > self.maximum_quantity:
            raise ValidationError({'minimum_quantity': 'La cantidad mínima no puede superar la máxima.'})
        if self.maximum_quantity and self.maximum_quantity < self.quantity:
            raise ValidationError({'maximum_quantity': 'La cantidad máxima no puede ser menor que la actual.'})

    def save(self, *args, **kwargs):
        database = kwargs.get('using') or router.db_for_write(type(self), instance=self)
        with transaction.atomic(using=database):
            if not self._state.adding:
                fields = kwargs.get('update_fields')
                original = type(self).objects.using(database).get(pk=self.pk)
                if (fields is None or 'quantity' in fields) and self.quantity != original.quantity:
                    raise ValidationError({'quantity': 'Modifique el saldo mediante un movimiento de inventario.'})
                if self.component_id != original.component_id:
                    raise ValidationError({'component': 'El stock no se puede trasladar a otro componente.'})
                # Validar límites con el saldo vigente y no reescribir cantidad al guardarlos.
                self.quantity = original.quantity
                kwargs['update_fields'] = (
                    [field for field in fields if field != 'quantity'] if fields is not None
                    else ['minimum_quantity', 'maximum_quantity', 'last_updated']
                )
            self.full_clean()
            super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.component.reference}: {self.quantity} unidades'


class StockMovementQuerySet(models.QuerySet):
    def delete(self):
        raise ValidationError('El historial no se elimina. Registre un movimiento compensatorio.')

    def update(self, **kwargs):
        raise ValidationError('Los movimientos registrados son inmutables.')

    def bulk_create(self, objs, **kwargs):
        raise ValidationError('Registre cada movimiento con save() para actualizar el saldo.')


class StockMovement(models.Model):
    ENTRY = 'entry'
    EXIT = 'exit'
    ADJUSTMENT = 'adjustment'
    MOVEMENT_TYPE_CHOICES = [
        (ENTRY, 'Entrada'),
        (EXIT, 'Salida'),
        (ADJUSTMENT, 'Ajuste'),
    ]

    stock = models.ForeignKey('inventory.Stock', on_delete=models.PROTECT, related_name='movements')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPE_CHOICES, default=ENTRY)
    quantity = models.IntegerField()
    reason = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = StockMovementQuerySet.as_manager()

    class Meta:
        ordering = ['-created_at']

    def clean(self):
        if not self._state.adding:
            self._check_immutable(self._state.db or 'default')
            return
        if self.quantity == 0:
            raise ValidationError({'quantity': 'La cantidad del movimiento debe ser distinta de cero.'})

        if not self.stock_id:
            return

        # Validar contra la base, nunca contra una relación cacheada por el formulario.
        self.stock = Stock.objects.using(self._state.db or 'default').get(pk=self.stock_id)

        if self.movement_type in {self.ENTRY, self.EXIT} and self.quantity < 0:
            raise ValidationError({'quantity': 'Las entradas y salidas deben ser cantidades positivas.'})

        if self.movement_type == self.ENTRY:
            if self.stock.maximum_quantity and self.stock.quantity + self.quantity > self.stock.maximum_quantity:
                raise ValidationError({'quantity': 'La entrada supera la cantidad máxima configurada.'})
            return

        if self.movement_type == self.EXIT:
            if self.quantity > self.stock.quantity:
                raise ValidationError({'quantity': 'No hay suficiente stock para realizar esta salida.'})
            return

        if self.movement_type == self.ADJUSTMENT:
            new_quantity = self.stock.quantity + self.quantity
            if new_quantity < 0:
                raise ValidationError({'quantity': 'El ajuste no puede dejar el stock en negativo.'})
            if self.stock.maximum_quantity and new_quantity > self.stock.maximum_quantity:
                raise ValidationError({'quantity': 'El ajuste supera la cantidad máxima configurada.'})

    def _check_immutable(self, database):
        original = type(self).objects.using(database).filter(pk=self.pk).first()
        if original is None:
            raise ValidationError('No se puede reconstruir un movimiento eliminado.')
        fields = ('stock_id', 'movement_type', 'quantity', 'reason', 'created_at')
        if any(getattr(self, field) != getattr(original, field) for field in fields):
            raise ValidationError('Los movimientos registrados son inmutables. Registre una corrección.')

    def save(self, *args, **kwargs):
        database = kwargs.get('using') or router.db_for_write(type(self), instance=self)
        if not self._state.adding:
            self._check_immutable(database)
            return
        if self.pk is not None and type(self).objects.using(database).filter(pk=self.pk).exists():
            raise ValidationError('Ya existe un movimiento con ese identificador.')
        self.full_clean()
        delta = -self.quantity if self.movement_type == self.EXIT else self.quantity
        try:
            with transaction.atomic(using=database):
                stock = Stock.objects.using(database).filter(pk=self.stock_id)
                if delta < 0:
                    stock = stock.filter(quantity__gte=-delta)
                else:
                    stock = stock.filter(Q(maximum_quantity=0) | Q(maximum_quantity__gte=F('quantity') + delta))
                updated = stock.update(quantity=F('quantity') + delta, last_updated=timezone.now())
                if updated != 1:
                    raise ValidationError({'quantity': 'El saldo cambió o el movimiento supera los límites. Revise la cantidad.'})
                super().save(*args, **kwargs)
        except Exception:
            # Un fallo de inserción revierte saldo y deja el objeto listo para corregir/reintentar.
            self.pk = None
            self._state.adding = True
            raise
        self.stock.refresh_from_db(using=database)

    def delete(self, *args, **kwargs):
        raise ValidationError('El historial no se elimina. Registre un movimiento compensatorio.')

    def __str__(self):
        return f'{self.stock.component.reference} - {self.get_movement_type_display()} ({self.quantity})'
