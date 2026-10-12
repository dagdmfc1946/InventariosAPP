from django.core.paginator import Paginator
from apps.documents.forms import DatasheetUploadForm


def component_detail_context(request, component, upload_form=None):
    movements = None
    if request.user.has_perm('inventory.view_stockmovement') and hasattr(component, 'stock'):
        movements = Paginator(component.stock.movements.order_by('-created_at', '-pk'), 25).get_page(request.GET.get('movements_page'))
    offers = component.supplier_offers.select_related('supplier') if request.user.has_perm('suppliers.view_supplieroffer') else []
    return {'component': component, 'upload_form': upload_form if upload_form is not None else DatasheetUploadForm(),
            'movements': movements, 'offers': offers}
