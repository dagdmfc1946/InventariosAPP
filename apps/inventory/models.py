from django.core.exceptions import ValidationError
from django.db import models


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
        if self.maximum_quantity and self.maximum_quantity < self.quantity:
            raise ValidationError({'maximum_quantity': 'La cantidad máxima no puede ser menor que la actual.'})

    def __str__(self):
        return f'{self.component.reference}: {self.quantity} unidades'


class StockMovement(models.Model):
    ENTRY = 'entry'
    EXIT = 'exit'
    ADJUSTMENT = 'adjustment'
    MOVEMENT_TYPE_CHOICES = [
        (ENTRY, 'Entrada'),
        (EXIT, 'Salida'),
        (ADJUSTMENT, 'Ajuste'),
    ]

    stock = models.ForeignKey('inventory.Stock', on_delete=models.CASCADE, related_name='movements')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPE_CHOICES, default=ENTRY)
    quantity = models.IntegerField()
    reason = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def clean(self):
        if self.quantity == 0:
            raise ValidationError({'quantity': 'La cantidad del movimiento debe ser distinta de cero.'})

    def __str__(self):
        return f'{self.stock.component.reference} - {self.get_movement_type_display()} ({self.quantity})'
