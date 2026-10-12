from django.db import transaction

from apps.inventory.models import Stock, StockMovement


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
