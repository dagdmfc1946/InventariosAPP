from django.core.management.base import BaseCommand
from apps.core.roles import configure_inventory_roles


class Command(BaseCommand):
    help = 'Crear/actualizar perfiles Lector y Operador; no asigna usuarios ni acceso administrativo.'

    def handle(self, *args, **options):
        roles = configure_inventory_roles()
        self.stdout.write(self.style.SUCCESS('Perfiles preparados: ' + ', '.join(group.name for group in roles.values())))
