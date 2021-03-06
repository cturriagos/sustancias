# Generated by Django 3.1.5 on 2021-08-08 19:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tecnicolaboratorio', '0009_remove_proyecto_responsable'),
        ('representantetecnico', '0016_auto_20210731_0036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solicitud',
            name='nombre_actividad',
        ),
        migrations.RemoveField(
            model_name='solicitud',
            name='responsable_actividad',
        ),
        migrations.RemoveField(
            model_name='solicitud',
            name='tipo_actividad',
        ),
        migrations.AddField(
            model_name='solicitud',
            name='proyecto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='tecnicolaboratorio.proyecto', verbose_name='Proyecto'),
        ),
    ]
