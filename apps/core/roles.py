from django.contrib.auth.models import Group, Permission


ROLE_NAMES = {'reader': 'Inventario - Lector', 'operator': 'Inventario - Operador'}


def configure_inventory_roles():
    readable = Permission.objects.filter(content_type__app_label__in=('components', 'inventory', 'documents', 'suppliers'), codename__startswith='view_')
    changes = {
        'components': ('add_component', 'change_component', 'add_category', 'add_specification', 'change_specification', 'delete_specification'),
        'inventory': ('add_location', 'change_location', 'add_stock', 'change_stock', 'add_stockmovement'),
        'documents': ('add_datasheet', 'change_datasheet'),
    }
    writable = []
    for app, codenames in changes.items():
        writable.extend(Permission.objects.filter(content_type__app_label=app, codename__in=codenames))
    result = {}
    for role, name in ROLE_NAMES.items():
        group, _ = Group.objects.get_or_create(name=name)
        group.permissions.set(list(readable) + (writable if role == 'operator' else []))
        result[role] = group
    return result
