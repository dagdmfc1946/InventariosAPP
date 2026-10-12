from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=120, unique=True)
    slug = models.SlugField(verbose_name='Identificador URL', max_length=120, unique=True, blank=True)
    description = models.TextField(verbose_name='Descripción', blank=True)
    created_at = models.DateTimeField(verbose_name='Fecha de creación', auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Component(models.Model):
    category = models.ForeignKey('components.Category', verbose_name='Categoría', on_delete=models.PROTECT, related_name='components')
    reference = models.CharField(verbose_name='Referencia', max_length=80, db_index=True)
    name = models.CharField(verbose_name='Nombre', max_length=200)
    value = models.CharField(verbose_name='Valor', max_length=120, blank=True)
    part_number = models.CharField(verbose_name='Número de parte', max_length=120, blank=True)
    is_active = models.BooleanField(verbose_name='Activo', default=True)
    created_at = models.DateTimeField(verbose_name='Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Última actualización', auto_now=True)

    class Meta:
        verbose_name = 'Componente'
        verbose_name_plural = 'Componentes'
        ordering = ['name', 'reference']
        constraints = [
            models.UniqueConstraint(fields=['category', 'reference'], name='unique_component_reference_per_category')
        ]

    def clean(self):
        if not self.name.strip():
            raise ValidationError({'name': 'El nombre del componente es obligatorio.'})

    def __str__(self):
        return f'{self.reference} - {self.name}'


class Specification(models.Model):
    component = models.ForeignKey('components.Component', verbose_name='Componente', on_delete=models.CASCADE, related_name='specifications')
    attribute = models.CharField(verbose_name='Atributo', max_length=120)
    value = models.CharField(verbose_name='Valor', max_length=255)
    unit = models.CharField(verbose_name='Unidad', max_length=30, blank=True)

    class Meta:
        verbose_name = 'Especificación'
        verbose_name_plural = 'Especificaciones'
        ordering = ['attribute']
        constraints = [
            models.UniqueConstraint(fields=['component', 'attribute'], name='unique_component_attribute')
        ]

    def clean(self):
        if not self.attribute.strip():
            raise ValidationError({'attribute': 'El nombre del atributo es obligatorio.'})
        if not self.value.strip():
            raise ValidationError({'value': 'El valor del atributo es obligatorio.'})

    def __str__(self):
        suffix = f' {self.unit}' if self.unit else ''
        return f'{self.component.reference}: {self.attribute} = {self.value}{suffix}'
