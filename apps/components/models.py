from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

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
    category = models.ForeignKey('components.Category', on_delete=models.PROTECT, related_name='components')
    reference = models.CharField(max_length=80, db_index=True)
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=120, blank=True)
    part_number = models.CharField(max_length=120, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
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
    component = models.ForeignKey('components.Component', on_delete=models.CASCADE, related_name='specifications')
    attribute = models.CharField(max_length=120)
    value = models.CharField(max_length=255)
    unit = models.CharField(max_length=30, blank=True)

    class Meta:
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
