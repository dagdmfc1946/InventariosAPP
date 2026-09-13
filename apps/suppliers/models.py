from django.core.exceptions import ValidationError
from django.db import models


class Supplier(models.Model):
    name = models.CharField(max_length=200, unique=True)
    contact = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def clean(self):
        if not self.name.strip():
            raise ValidationError({'name': 'El nombre del proveedor es obligatorio.'})

    def __str__(self):
        return self.name


class SupplierOffer(models.Model):
    component = models.ForeignKey('components.Component', on_delete=models.CASCADE, related_name='supplier_offers')
    supplier = models.ForeignKey('suppliers.Supplier', on_delete=models.PROTECT, related_name='offers')
    part_number = models.CharField(max_length=120, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    currency = models.CharField(max_length=10, default='EUR')
    minimum_quantity = models.PositiveIntegerField(default=1)
    url = models.URLField(blank=True)
    date_consulted = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['supplier__name', '-date_consulted']
        constraints = [
            models.UniqueConstraint(fields=['component', 'supplier', 'part_number'], name='unique_supplier_offer')
        ]

    def clean(self):
        errors = {}
        if self.price < 0:
            errors['price'] = 'El precio no puede ser negativo.'
        if self.minimum_quantity < 1:
            errors['minimum_quantity'] = 'La cantidad mínima debe ser mayor que cero.'
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f'{self.supplier.name} - {self.component.reference}'
