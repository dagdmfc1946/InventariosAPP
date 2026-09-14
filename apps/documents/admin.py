from django.contrib import admin
from django.utils.html import format_html

from .models import Datasheet


@admin.register(Datasheet)
class DatasheetAdmin(admin.ModelAdmin):
    list_display = ('component', 'file', 'preview_link', 'uploaded_at')
    search_fields = ('component__reference', 'component__name', 'file')
    list_filter = ('uploaded_at',)

    @admin.display(description='Visualizar')
    def preview_link(self, obj):
        if not obj.file:
            return '-'
        return format_html(
            '<a href="{}" target="_blank" rel="noopener">Abrir PDF</a>',
            obj.file.url,
        )
