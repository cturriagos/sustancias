# Generated by Django 3.1.5 on 2021-08-26 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representantetecnico', '0029_remove_solicitud_documento_solicitud'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitud',
            name='documento_solicitud',
            field=models.FileField(null=True, upload_to='solicitud/%Y/%m/%d'),
        ),
    ]
