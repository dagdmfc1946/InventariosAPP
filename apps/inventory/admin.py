from django.contrib import admin

from .models import Location, Stock, StockMovement


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('component', 'shelf', 'box', 'drawer', 'description')
    search_fields = ('component__reference', 'component__name', 'shelf', 'box', 'drawer', 'description')
    list_filter = ('shelf', 'box')


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('component', 'quantity', 'minimum_quantity', 'maximum_quantity', 'last_updated')
    search_fields = ('component__reference', 'component__name')
    list_filter = ('minimum_quantity',)


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('stock', 'movement_type', 'quantity', 'reason', 'created_at')
    list_filter = ('movement_type',)
    search_fields = ('stock__component__reference', 'reason')
