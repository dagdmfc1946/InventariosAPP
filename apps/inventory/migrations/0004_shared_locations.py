from django.db import migrations
from django.db.migrations.exceptions import IrreversibleError


def preserve_assignments(apps, schema_editor):
    Location = apps.get_model('inventory', 'Location')
    Component = apps.get_model('components', 'Component')
    database = schema_editor.connection.alias
    for location in Location.objects.using(database).exclude(component_id=None).iterator():
        Component.objects.using(database).filter(pk=location.component_id).update(location_id=location.pk)


def restore_assignments(apps, schema_editor):
    Location = apps.get_model('inventory', 'Location')
    Component = apps.get_model('components', 'Component')
    database = schema_editor.connection.alias
    for location in Location.objects.using(database).all():
        components = Component.objects.using(database).filter(location_id=location.pk)
        if components.count() > 1:
            raise IrreversibleError('Una ubicación compartida no cabe en el modelo anterior. Restaure el respaldo de Fase 1.')
        Location.objects.using(database).filter(pk=location.pk).update(component_id=components.values_list('pk', flat=True).first())


class Migration(migrations.Migration):
    dependencies = [('components', '0003_component_location'), ('inventory', '0003_spanish_interface')]
    operations = [migrations.RunPython(preserve_assignments, restore_assignments),
                  migrations.RemoveField(model_name='location', name='component')]
