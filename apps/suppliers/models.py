from django.core.exceptions import ValidationError
from django.db import models


class Supplier(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=200, unique=True)
    contact = models.CharField(verbose_name='Contacto', max_length=120, blank=True)
    phone = models.CharField(verbose_name='Teléfono', max_length=40, blank=True)
    email = models.EmailField(verbose_name='Correo electrónico', blank=True)
    website = models.URLField(verbose_name='Sitio web', blank=True)
    notes = models.TextField(verbose_name='Notas', blank=True)
    created_at = models.DateTimeField(verbose_name='Fecha de creación', auto_now_add=True)

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['name']

    def clean(self):
        if not self.name.strip():
            raise ValidationError({'name': 'El nombre del proveedor es obligatorio.'})

    def __str__(self):
        return self.name


class SupplierOffer(models.Model):
    component = models.ForeignKey('components.Component', verbose_name='Componente', on_delete=models.CASCADE, related_name='supplier_offers')
    supplier = models.ForeignKey('suppliers.Supplier', verbose_name='Proveedor', on_delete=models.PROTECT, related_name='offers')
    part_number = models.CharField(verbose_name='Número de parte', max_length=120, blank=True)
    price = models.DecimalField(verbose_name='Precio', max_digits=12, decimal_places=4, default=0)
    currency = models.CharField(verbose_name='Moneda', max_length=10, default='EUR')
    minimum_quantity = models.PositiveIntegerField(verbose_name='Cantidad mínima de compra', default=1)
    url = models.URLField(verbose_name='Enlace', blank=True)
    date_consulted = models.DateField(verbose_name='Fecha de consulta', blank=True, null=True)
    notes = models.TextField(verbose_name='Notas', blank=True)

    class Meta:
        verbose_name = 'Oferta de proveedor'
        verbose_name_plural = 'Ofertas de proveedores'
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
