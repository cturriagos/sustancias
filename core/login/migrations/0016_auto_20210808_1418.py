# Generated by Django 3.1.5 on 2021-08-08 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tecnicolaboratorio', '0009_remove_proyecto_responsable'),
        ('representantetecnico', '0017_auto_20210808_1418'),
        ('login', '0015_user_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='persona',
        ),
        migrations.DeleteModel(
            name='Persona',
        ),
        migrations.DeleteModel(
            name='TipoPersona',
        ),
    ]