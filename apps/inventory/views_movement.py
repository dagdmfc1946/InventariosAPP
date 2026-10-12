from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ValidationError
from django.db import DatabaseError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from apps.components.models import Component
from apps.core.access import inventory_read_required
from .forms_movement import MovementForm
from .services import register_component_movement


@inventory_read_required
@permission_required('inventory.add_stockmovement', raise_exception=True)
@require_http_methods(['GET', 'POST'])
def component_movement(request, pk):
    component = get_object_or_404(Component.objects.select_related('stock'), pk=pk)
    form = MovementForm(request.POST if request.method == 'POST' else None, component=component, user=request.user)
    preview = False
    if request.method == 'POST' and form.is_valid():
        if request.POST.get('action') == 'preview':
            preview = True
        else:
            try:
                _, created = register_component_movement(component, request.user, form.cleaned_data, form.operation)
            except ValidationError as error:
                form.add_error(None, error.messages)
            except DatabaseError:
                form.add_error(None, 'No se pudo confirmar el movimiento. Recarga la ficha y comprueba el historial antes de reintentar.')
            else:
                messages.success(request, 'Movimiento registrado.' if created else 'Este movimiento ya estaba registrado; no se aplicó nuevamente.')
                return redirect('component_detail', pk=component.pk)
    return render(request, 'inventory/component_movement.html', {'component': component, 'form': form, 'preview': preview})
