from django.contrib import admin

from .models import Supplier, SupplierOffer


class SupplierOfferInline(admin.TabularInline):
    model = SupplierOffer
    extra = 1


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'email', 'phone')
    search_fields = ('name', 'contact', 'email')


@admin.register(SupplierOffer)
class SupplierOfferAdmin(admin.ModelAdmin):
    list_display = ('component', 'supplier', 'price', 'currency', 'minimum_quantity', 'date_consulted')
    list_filter = ('supplier', 'currency')
    search_fields = ('component__reference', 'component__name', 'supplier__name', 'part_number')
