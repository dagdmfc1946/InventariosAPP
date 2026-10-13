import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('components', '0002_spanish_interface'), ('inventory', '0003_spanish_interface')]
    operations = [migrations.AddField(
        model_name='component', name='location',
        field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT,
                                related_name='components', to='inventory.location', verbose_name='Ubicación'),
    )]
