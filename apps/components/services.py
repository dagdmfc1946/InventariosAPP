from django.db import transaction

from apps.inventory.models import Stock, StockMovement
from django.core.exceptions import ValidationError
from .models import Component, Specification


@transaction.atomic
def create_component_with_stock(component, *, initial_quantity=0, minimum_quantity=0, maximum_quantity=0):
    """Alta completa: ningún registro queda guardado si falla el stock inicial."""
    component.full_clean()
    component.save()
    stock = Stock(
        component=component, quantity=initial_quantity,
        minimum_quantity=minimum_quantity, maximum_quantity=maximum_quantity,
    )
    stock.full_clean()
    stock.quantity = 0
    stock.save()
    if initial_quantity:
        StockMovement.objects.create(
            stock=stock, movement_type=StockMovement.ENTRY,
            quantity=initial_quantity, reason='Stock inicial al registrar el componente',
        )
    return component


@transaction.atomic
def duplicate_component(source, *, reference, name):
    if reference == source.reference:
        raise ValidationError('La nueva referencia debe ser diferente de la original.')
    component = create_component_with_stock(Component(category=source.category, reference=reference,
        name=name, value=source.value, part_number=source.part_number))
    for original in source.specifications.all():
        specification = Specification(component=component, attribute=original.attribute, value=original.value, unit=original.unit)
        specification.full_clean()
        specification.save()
    return component
