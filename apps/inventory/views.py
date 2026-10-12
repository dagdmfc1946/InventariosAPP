from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from apps.core.access import inventory_read_required
from .forms import LocationForm
from .models import Location
from .services import assign_location_components


@inventory_read_required
@permission_required('inventory.view_location', raise_exception=True)
@require_http_methods(['GET'])
def location_list(request):
    return render(request, 'inventory/location_list.html', {'locations': Location.objects.prefetch_related('components')})


@inventory_read_required
@require_http_methods(['GET', 'POST'])
def location_edit(request, pk=None):
    permission = 'inventory.change_location' if pk else 'inventory.add_location'
    if not request.user.has_perm(permission):
        raise PermissionDenied
    location = get_object_or_404(Location, pk=pk) if pk else Location()
    form = LocationForm(request.POST if request.method == 'POST' else None, instance=location)
    can_assign = request.user.has_perm('components.change_component')
    form.fields['components'].disabled = not can_assign
    if request.method == 'POST' and form.is_valid():
        with transaction.atomic():
            location = form.save()
            if can_assign:
                assign_location_components(location, form.cleaned_data['components'])
        messages.success(request, 'Ubicación guardada y componentes asignados.')
        return redirect('location_list')
    return render(request, 'inventory/location_edit.html', {'form': form, 'location': location})
