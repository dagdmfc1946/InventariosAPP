from django.contrib import admin

from .models import Datasheet


@admin.register(Datasheet)
class DatasheetAdmin(admin.ModelAdmin):
    list_display = ('component', 'file', 'uploaded_at')
    search_fields = ('component__reference', 'component__name', 'file')
    list_filter = ('uploaded_at',)
