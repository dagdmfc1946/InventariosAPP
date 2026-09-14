from django.db.models import Q
from django.shortcuts import redirect, render

from apps.components.models import Component


def site_home(request):
    return redirect('component_search')


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
