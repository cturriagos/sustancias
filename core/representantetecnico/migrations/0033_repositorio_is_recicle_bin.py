# Generated by Django 3.1.5 on 2021-08-26 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representantetecnico', '0032_auto_20210826_0215'),
    ]

    operations = [
        migrations.AddField(
            model_name='repositorio',
            name='is_recicle_bin',
            field=models.BooleanField(default=False),
        ),
    ]