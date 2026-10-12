from django.db.models import Q, F
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect, render
from .forms import ProfileForm
from .access import inventory_read_required

from apps.components.models import Category, Component


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
    if ordering not in ('name', 'stock', '-stock'):
        ordering = 'name'
    category = request.GET.get('category', '')
    availability = request.GET.get('availability', '')
    attention = request.GET.get('attention', '')

    components = Component.objects.select_related('category', 'stock').filter(is_active=True)

    if category.isdecimal() and len(category) <= 19 and int(category) <= 9223372036854775807:
        components = components.filter(category_id=category)
    else:
        category = ''
    if availability == 'available':
        components = components.filter(stock__quantity__gt=0)
    elif availability == 'empty':
        components = components.filter(Q(stock__quantity=0) | Q(stock__isnull=True))
    else:
        availability = ''
    if attention == 'low':
        components = components.filter(stock__quantity__lte=F('stock__minimum_quantity'))
    elif attention == 'no_pdf':
        components = components.filter(datasheets__isnull=True)
    elif attention == 'no_offer':
        components = components.filter(supplier_offers__isnull=True)
    else:
        attention = ''

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

    page = Paginator(components, 25).get_page(request.GET.get('page'))
    params = request.GET.copy()
    params.pop('page', None)
    return render(request, 'core/component_search.html', {
        'components': page, 'page_obj': page, 'pagination_query': params.urlencode(),
        'categories': Category.objects.all(), 'selected_category': category,
        'availability': availability, 'attention': attention,
        'q': query,
        'ordering': ordering,
    })
