from django.db import transaction
from apps.components.models import Component
from django.core.exceptions import PermissionDenied, ValidationError
from .models import Stock, StockMovement


@transaction.atomic
def assign_location_components(location, components):
    ids = [component.pk for component in components]
    Component.objects.filter(location=location).exclude(pk__in=ids).update(location=None)
    Component.objects.filter(pk__in=ids).update(location=location)


@transaction.atomic
def register_component_movement(component, user, data, operation):
    previous = StockMovement.objects.filter(request_id=operation['request']).first()
    if previous:
        if (previous.stock.component_id != component.pk or previous.movement_type != data['movement_type']
                or previous.quantity != data['quantity'] or previous.reason != data['reason']):
            raise ValidationError('Este formulario ya se utilizó para otro movimiento. Recarga la ficha.')
        return previous, False
    stock = Stock.objects.filter(component=component).first()
    if stock is None:
        if not user.has_perm('inventory.add_stock'):
            raise PermissionDenied
        stock = Stock.objects.create(component=component)
    if stock.quantity != operation['balance']:
        raise ValidationError('El saldo cambió desde que abriste la ficha. Recarga y revisa el movimiento.')
    movement = StockMovement(stock=stock, movement_type=data['movement_type'], quantity=data['quantity'],
        reason=data['reason'], request_id=operation['request'])
    movement.save()
    return movement, True
