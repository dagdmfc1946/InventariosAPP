from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import DatabaseError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from apps.core.access import inventory_read_required
from .forms_duplicate import ComponentDuplicateForm
from .models import Component
from .services import duplicate_component


@inventory_read_required
@permission_required(('components.add_component', 'inventory.add_stock'), raise_exception=True)
@require_http_methods(['GET', 'POST'])
def component_duplicate(request, pk):
    source = get_object_or_404(Component, pk=pk)
    if source.specifications.exists() and not request.user.has_perm('components.add_specification'):
        raise PermissionDenied
    form = ComponentDuplicateForm(request.POST if request.method == 'POST' else None, initial={'name': source.name})
    if request.method == 'POST' and form.is_valid():
        try:
            component = duplicate_component(source, **form.cleaned_data)
        except ValidationError as error:
            form.add_error(None, error.messages)
        except DatabaseError:
            form.add_error(None, 'No se pudo duplicar. Comprueba si la referencia ya existe e intenta nuevamente.')
        else:
            messages.success(request, 'Componente duplicado con existencias cero. Revisa su ficha y asigna ubicación si lo necesitas.')
            return redirect('component_detail', pk=component.pk)
    return render(request, 'components/component_duplicate.html', {'component': source, 'form': form})
