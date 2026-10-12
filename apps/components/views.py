from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .forms import ComponentQuickCreateForm
from .models import Category
from .services import create_component_with_stock


@login_required
@permission_required(('components.add_component', 'inventory.add_stock', 'inventory.add_stockmovement'), raise_exception=True)
@require_http_methods(['GET', 'POST'])
def component_create(request):
    form = ComponentQuickCreateForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        try:
            component = create_component_with_stock(
                form.save(commit=False),
                initial_quantity=form.cleaned_data['initial_quantity'],
                minimum_quantity=form.cleaned_data['minimum_quantity'],
                maximum_quantity=form.cleaned_data['maximum_quantity'],
            )
        except ValidationError as error:
            if hasattr(error, 'message_dict'):
                for field, errors in error.message_dict.items():
                    target = 'initial_quantity' if field == 'quantity' else field
                    form.add_error(target if target in form.fields else None, errors)
            else:
                form.add_error(None, error.messages)
        except IntegrityError:
            # También controla envíos concurrentes: el servicio revierte toda la operación.
            form.add_error(None, 'No se pudo registrar. Comprueba que la referencia no exista en esta categoría.')
        else:
            messages.success(request, f'{component.reference} · {component.name} guardado con sus existencias iniciales.')
            if 'save_another' in request.POST:
                return redirect('component_create')
            return redirect('component_search')
    return render(request, 'components/component_create.html', {
        'form': form, 'has_categories': Category.objects.exists(),
    })
