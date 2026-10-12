from django.db.models import Q, F
from django.db import IntegrityError, transaction
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
        try:
            with transaction.atomic():
                profile.save(update_fields=['username', 'first_name', 'last_name', 'email'])
        except IntegrityError:
            form.add_error('username', 'No se pudo guardar ese nombre de usuario. Elige otro e inténtalo nuevamente.')
        else:
            messages.success(request, 'Tus datos de perfil se actualizaron. Usa tu nombre de usuario actualizado para iniciar sesión.')
            return redirect('profile_edit')
    if request.method == 'POST':
        request.user.refresh_from_db(fields=['username', 'first_name', 'last_name', 'email'])
    return render(request, 'registration/profile.html', {'form': form})


def site_home(request):
    return redirect('component_search')


def filtered_components(params):
    query = params.get('q', '').strip()
    ordering = params.get('ordering', 'name')
    if ordering not in ('name', 'stock', '-stock'):
        ordering = 'name'
    category = params.get('category', '')
    availability = params.get('availability', '')
    attention = params.get('attention', '')

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
        components = components.order_by('-stock__quantity', 'name', 'reference', 'pk')
    elif ordering == 'stock':
        components = components.order_by('stock__quantity', 'name', 'reference', 'pk')
    else:
        components = components.order_by('name', 'reference', 'pk')

    return components, {'selected_category': category, 'availability': availability, 'attention': attention, 'q': query, 'ordering': ordering}


@inventory_read_required
def component_search(request):
    components, filters = filtered_components(request.GET)
    page = Paginator(components, 25).get_page(request.GET.get('page'))
    params = request.GET.copy()
    params.pop('page', None)
    return render(request, 'core/component_search.html', {
        'components': page, 'page_obj': page, 'pagination_query': params.urlencode(),
        'categories': Category.objects.all(), **filters,
    })


@inventory_read_required
@require_http_methods(['GET'])
def component_export_pdf(request):
    from django.http import HttpResponse
    from django.utils import timezone
    from .pdf_catalog import build_catalog_pdf

    components, filters = filtered_components(request.GET)
    # Materializar una consulta: filas y total corresponden a la misma lectura.
    rows = list(components.select_related('location'))
    response = HttpResponse(build_catalog_pdf(rows, filters), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="componentes-{timezone.localdate():%Y-%m-%d}.pdf"'
    response['Cache-Control'] = 'private, no-store'
    response['X-Content-Type-Options'] = 'nosniff'
    return response
