from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect, render
from .forms import ProfileForm
from .access import inventory_read_required

from apps.components.models import Component


@login_required
@require_http_methods(['GET', 'POST'])
def profile_edit(request):
    form = ProfileForm(request.POST if request.method == 'POST' else None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        profile = form.save(commit=False)
        profile.save(update_fields=['first_name', 'last_name', 'email'])
        messages.success(request, 'Tus datos de perfil se actualizaron.')
        return redirect('profile_edit')
    return render(request, 'registration/profile.html', {'form': form})


def site_home(request):
    return redirect('component_search')


@inventory_read_required
def component_search(request):
    query = request.GET.get('q', '').strip()
    ordering = request.GET.get('ordering', 'name')

    components = Component.objects.select_related('category', 'stock').filter(is_active=True)

    if query:
        components = components.filter(
            Q(name__icontains=query)
            | Q(reference__icontains=query)
            | Q(value__icontains=query)
            | Q(part_number__icontains=query)
            | Q(category__name__icontains=query)
        )

    if ordering == '-stock':
        components = components.order_by('-stock__quantity', 'name', 'reference')
    elif ordering == 'stock':
        components = components.order_by('stock__quantity', 'name', 'reference')
    else:
        components = components.order_by('name', 'reference')

    return render(request, 'core/component_search.html', {
        'components': components,
        'q': query,
        'ordering': ordering,
    })
