from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group


def permission_label(permission):
    model = permission.content_type.model_class()
    action = permission.codename.split('_', 1)[0]
    verbs = {'add': 'agregar', 'change': 'modificar', 'delete': 'eliminar', 'view': 'consultar'}
    if model and action in verbs:
        return f'{model._meta.app_config.verbose_name} | {model._meta.verbose_name} | Puede {verbs[action]}'
    return permission.name


class SpanishPermissionLabels:
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        field = super().formfield_for_manytomany(db_field, request, **kwargs)
        if db_field.name in ('user_permissions', 'permissions'):
            field.label_from_instance = permission_label
        return field


class ApplicationUserAdmin(SpanishPermissionLabels, UserAdmin):
    """Las altas desde la interfaz crean cuentas normales con contraseña usable."""

    add_form = UserCreationForm
    add_fieldsets = ((None, {'classes': ('wide',), 'fields': ('username', 'password1', 'password2')}),)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Datos personales', {'fields': ('first_name', 'last_name', 'email')}),
        ('Acceso al aplicativo', {'fields': ('is_active', 'groups', 'user_permissions')}),
        ('Fechas', {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ('last_login', 'date_joined')
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active')
    list_filter = ('is_active', 'groups')
    add_form_template = 'admin/auth/user/application_add_form.html'

    def has_module_permission(self, request):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser and not (obj and obj.is_superuser)

    def get_actions(self, request):
        # Evitar que la eliminación masiva se salte la protección por objeto.
        actions = super().get_actions(request)
        actions.pop('delete_selected', None)
        return actions


admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), ApplicationUserAdmin)


class ApplicationGroupAdmin(SpanishPermissionLabels, GroupAdmin):
    pass


admin.site.unregister(Group)
admin.site.register(Group, ApplicationGroupAdmin)
admin.site.site_header = 'InventariosAPP'
admin.site.site_title = 'InventariosAPP'
admin.site.index_title = 'Administración del inventario'
admin.site.site_url = '/search/'
