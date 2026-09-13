from django.db.models import Count, F
from django.shortcuts import render

from apps.components.models import Component
from apps.inventory.models import StockMovement


def dashboard(request):
    low_stock_count = Component.objects.filter(is_active=True).filter(
        stock__quantity__lte=F('stock__minimum_quantity')
    ).count()

    missing_datasheets_count = Component.objects.filter(is_active=True).annotate(
        datasheet_count=Count('datasheets')
    ).filter(datasheet_count=0).count()

    missing_prices_count = Component.objects.filter(is_active=True).annotate(
        offer_count=Count('supplier_offers')
    ).filter(offer_count=0).count()

    recent_movements = StockMovement.objects.select_related('stock__component').order_by('-created_at')[:10]

    return render(request, 'dashboard/dashboard.html', {
        'low_stock_count': low_stock_count,
        'missing_datasheets_count': missing_datasheets_count,
        'missing_prices_count': missing_prices_count,
        'recent_movements': recent_movements,
    })
