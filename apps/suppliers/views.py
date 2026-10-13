from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.paginator import Paginator
from django.db import DatabaseError, transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from apps.components.models import Component
from apps.core.access import inventory_read_required
from .forms import SupplierForm, SupplierOfferForm
from .models import Supplier, SupplierOffer


@inventory_read_required
@permission_required('suppliers.view_supplier', raise_exception=True)
@require_http_methods(['GET'])
def supplier_list(request):
    query = request.GET.get('q', '').strip()
    suppliers = Supplier.objects.filter(name__icontains=query)
    page = Paginator(suppliers, 25).get_page(request.GET.get('page'))
    return render(request, 'suppliers/supplier_list.html', {'page_obj': page, 'q': query})


@inventory_read_required
@require_http_methods(['GET', 'POST'])
def supplier_edit(request, pk=None):
    required = 'suppliers.change_supplier' if pk is not None else 'suppliers.add_supplier'
    if not request.user.has_perm(required):
        raise PermissionDenied
    supplier = get_object_or_404(Supplier, pk=pk) if pk is not None else Supplier()
    form = SupplierForm(request.POST if request.method == 'POST' else None, instance=supplier)
    if request.method == 'POST' and form.is_valid():
        try:
            with transaction.atomic():
                form.save()
        except DatabaseError:
            form.add_error(None, 'No se pudo guardar el proveedor. Comprueba nombres duplicados e intenta nuevamente.')
        else:
            messages.success(request, 'Proveedor guardado.')
            return redirect('supplier_list')
    return render(request, 'suppliers/supplier_edit.html', {'form': form, 'supplier': supplier})


@inventory_read_required
@require_http_methods(['GET', 'POST'])
def offer_edit(request, component_pk, pk=None):
    required = 'suppliers.change_supplieroffer' if pk is not None else 'suppliers.add_supplieroffer'
    if not request.user.has_perm(required):
        raise PermissionDenied
    component = get_object_or_404(Component, pk=component_pk)
    offer = get_object_or_404(SupplierOffer, pk=pk, component=component) if pk is not None else SupplierOffer(component=component)
    data = request.POST.copy() if request.method == 'POST' else None
    supplier_action = request.method == 'POST' and request.POST.get('action') == 'create_supplier'
    supplier_form = SupplierForm(data if supplier_action else None, prefix='supplier')
    # El proveedor contextual es opcional al guardar la oferta; validar required en servidor al crearlo.
    supplier_form.use_required_attribute = False
    if supplier_action:
        if not request.user.has_perm('suppliers.add_supplier'):
            raise PermissionDenied
        if supplier_form.is_valid():
            try:
                with transaction.atomic():
                    supplier = supplier_form.save()
            except DatabaseError:
                supplier_form.add_error(None, 'No se pudo crear el proveedor. Comprueba nombres duplicados e intenta nuevamente.')
            else:
                data['supplier'] = str(supplier.pk)
                messages.success(request, 'Proveedor creado y seleccionado. Guarda la oferta para confirmarla.')
                supplier_form = SupplierForm(prefix='supplier')
                supplier_form.use_required_attribute = False
    form = SupplierOfferForm(data, instance=offer)
    if request.method == 'POST' and not supplier_action and form.is_valid():
        try:
            with transaction.atomic():
                offer = form.save(commit=False)
                offer.full_clean()
                offer.save()
        except ValidationError as error:
            form.add_error(None, error.messages)
        except DatabaseError:
            form.add_error(None, 'No se pudo guardar. Comprueba proveedor y número de parte duplicados e intenta nuevamente.')
        else:
            messages.success(request, 'Oferta guardada.')
            return redirect('component_detail', pk=component.pk)
    return render(request, 'suppliers/offer_edit.html', {'form': form, 'component': component, 'offer': offer, 'supplier_form': supplier_form})
