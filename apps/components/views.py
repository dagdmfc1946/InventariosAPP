from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import CategoryContextForm, ComponentEditForm, ComponentQuickCreateForm, SpecificationFormSet
from .models import Category, Component
from apps.core.access import inventory_read_required
from .services import create_component_with_stock


@login_required
@permission_required(('components.add_component', 'inventory.add_stock', 'inventory.add_stockmovement'), raise_exception=True)
@require_http_methods(['GET', 'POST'])
def component_create(request):
    data, category_form, category_action = handle_category_action(request)
    data, location_form, location_action = handle_location_action(request, data)
    form = ComponentQuickCreateForm(data)
    if request.method == 'POST' and not category_action and not location_action and form.is_valid():
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
        'category_form': category_form,
        'location_form': location_form,
    })


def handle_category_action(request):
    data = request.POST.copy() if request.method == 'POST' else None
    handled = request.method == 'POST' and request.POST.get('action') == 'create_category'
    category_form = CategoryContextForm(data if handled else None, prefix='category')
    if handled:
        if not request.user.has_perm('components.add_category'):
            raise PermissionDenied
        if category_form.is_valid():
            try:
                with transaction.atomic():
                    category_form.category.save()
            except IntegrityError:
                category_form.add_error('name', 'Esa categoría o identificador ya existe. Elige otro nombre.')
            else:
                data['category'] = str(category_form.category.pk)
                messages.success(request, 'Categoría creada y seleccionada. Tus datos siguen en el formulario; guarda el componente para confirmarlos.')
                category_form = CategoryContextForm(prefix='category')
    return data, category_form, handled


def handle_location_action(request, data):
    from apps.inventory.forms_context import LocationContextForm
    handled = request.method == 'POST' and request.POST.get('action') == 'create_location'
    form = LocationContextForm(data if handled else None, prefix='location')
    if handled:
        if not request.user.has_perm('inventory.add_location'):
            raise PermissionDenied
        if form.is_valid():
            location = form.save()
            data['location'] = str(location.pk)
            messages.success(request, 'Ubicación creada y seleccionada. Guarda el componente para confirmar la asignación.')
            form = LocationContextForm(prefix='location')
    return data, form, handled


@inventory_read_required
@require_http_methods(['GET'])
def component_detail(request, pk):
    component = get_object_or_404(Component.objects.select_related('category', 'location', 'stock').prefetch_related('specifications', 'datasheets'), pk=pk)
    from apps.documents.forms import DatasheetUploadForm
    return render(request, 'components/component_detail.html', {'component': component, 'upload_form': DatasheetUploadForm()})


@login_required
@permission_required('components.change_component', raise_exception=True)
@require_http_methods(['GET', 'POST'])
def component_edit(request, pk):
    component = get_object_or_404(Component, pk=pk)
    data, category_form, category_action = handle_category_action(request)
    data, location_form, location_action = handle_location_action(request, data)
    add_row = request.method == 'POST' and request.POST.get('action') == 'add_spec_row'
    if add_row:
        try:
            count = int(data.get('specifications-TOTAL_FORMS', '0'))
        except ValueError:
            count = 0
        data['specifications-TOTAL_FORMS'] = str(min(max(count, 0) + 1, 50))
    form = ComponentEditForm(data, instance=component)
    formset = SpecificationFormSet(data, instance=component, prefix='specifications')
    for row in formset.forms:
        row.fields['id'].queryset = component.specifications.all()
    if request.method == 'POST' and not category_action and not location_action and not add_row:
        valid_form = form.is_valid()
        valid_specs = formset.is_valid()
        if valid_form and valid_specs:
            for row in formset.forms:
                if not row.has_changed():
                    continue
                deleting = row.cleaned_data.get('DELETE')
                if not row.instance.pk and deleting:
                    continue
                action = 'delete' if deleting else ('change' if row.instance.pk else 'add')
                if not request.user.has_perm(f'components.{action}_specification'):
                    raise PermissionDenied
            try:
                with transaction.atomic():
                    form.save()
                    formset.save()
            except IntegrityError:
                form.add_error(None, 'No se pudo guardar. Comprueba referencias y atributos duplicados.')
            else:
                messages.success(request, 'Ficha actualizada. Las existencias no se modificaron.')
                return redirect('component_detail', pk=component.pk)
    return render(request, 'components/component_edit.html', {
        'component': component, 'form': form, 'formset': formset, 'category_form': category_form,
        'location_form': location_form,
    })
