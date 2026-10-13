from django.contrib import admin
from django.core.exceptions import PermissionDenied
from .forms import LocationForm

from .models import Location, Stock, StockMovement


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    form = LocationForm
    list_display = ('shelf', 'box', 'drawer', 'description', 'component_count')
    search_fields = ('components__reference', 'components__name', 'shelf', 'box', 'drawer', 'description')
    list_filter = ('shelf', 'box')

    @admin.display(description='Componentes')
    def component_count(self, obj):
        return obj.components.count()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['components'].disabled = not request.user.has_perm('components.change_component')
        return form

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        if 'components' in form.changed_data:
            if not request.user.has_perm('components.change_component'):
                raise PermissionDenied
            from .services import assign_location_components
            assign_location_components(form.instance, form.cleaned_data['components'])


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('component', 'quantity', 'minimum_quantity', 'maximum_quantity', 'last_updated')
    search_fields = ('component__reference', 'component__name')
    list_filter = ('minimum_quantity',)

    def get_readonly_fields(self, request, obj=None):
        return ('quantity', 'component') if obj else ()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('stock', 'movement_type', 'quantity', 'reason', 'created_at')
    list_filter = ('movement_type',)
    search_fields = ('stock__component__reference', 'reason')

    def has_change_permission(self, request, obj=None):
        return False if obj else super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return False
