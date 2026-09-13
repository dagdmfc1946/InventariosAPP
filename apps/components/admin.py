from django.contrib import admin

from .models import Category, Component, Specification


class SpecificationInline(admin.TabularInline):
    model = Specification
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('reference', 'name', 'category', 'value', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('reference', 'name', 'part_number', 'value')
    inlines = [SpecificationInline]
    fields = ('category', 'reference', 'name', 'value', 'part_number', 'is_active')


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ('component', 'attribute', 'value', 'unit')
    list_filter = ('attribute',)
    search_fields = ('component__reference', 'component__name', 'attribute', 'value')
