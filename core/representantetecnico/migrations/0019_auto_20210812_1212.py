# Generated by Django 3.1.5 on 2021-08-12 17:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('representantetecnico', '0018_auto_20210812_0039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='sustancia',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='representantetecnico.sustancia'),
        ),
    ]
