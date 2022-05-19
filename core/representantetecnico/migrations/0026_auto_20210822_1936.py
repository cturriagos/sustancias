# Generated by Django 3.1.5 on 2021-08-23 00:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('representantetecnico', '0025_remove_solicituddetalle_cantidad_consumida'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compraspublicas',
            name='user_creation',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_creation_representantetecnico_compraspublicas_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='compraspublicas',
            name='user_updated',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_updated_representantetecnico_compraspublicas_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='compraspublicasdetalle',
            name='user_creation',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_creation_representantetecnico_compraspublicasdetalle_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='compraspublicasdetalle',
            name='user_updated',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_updated_representantetecnico_compraspublicasdetalle_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='desgloseinfomemensualdetalle',
            name='user_creation',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_creation_representantetecnico_desgloseinfomemensualdetalle_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='desgloseinfomemensualdetalle',
            name='user_updated',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_updated_representantetecnico_desgloseinfomemensualdetalle_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='informesmensuales',
            name='user_creation',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_creation_representantetecnico_informesmensuales_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='informesmensuales',
            name='user_updated',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_updated_representantetecnico_informesmensuales_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='informesmensualesdetalle',
            name='user_creation',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_creation_representantetecnico_informesmensualesdetalle_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='informesmensualesdetalle',
            name='user_updated',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_updated_representantetecnico_informesmensualesdetalle_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='inventario',
            name='user_creation',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_creation_representantetecnico_inventario_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='inventario',
            name='user_updated',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_updated_representantetecnico_inventario_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='user_creation',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_creation_representantetecnico_proveedor_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='user_updated',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_updated_representantetecnico_proveedor_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='repositorio',
            name='user_creation',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_creation_representantetecnico_repositorio_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='repositorio',
            name='user_updated',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_updated_representantetecnico_repositorio_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='user_creation',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_creation_representantetecnico_solicitud_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='user_updated',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_updated_representantetecnico_solicitud_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='solicituddetalle',
            name='user_creation',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_creation_representantetecnico_solicituddetalle_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='solicituddetalle',
            name='user_updated',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_updated_representantetecnico_solicituddetalle_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='stock',
            name='user_creation',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_creation_representantetecnico_stock_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='stock',
            name='user_updated',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_updated_representantetecnico_stock_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='sustancia',
            name='user_creation',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_creation_representantetecnico_sustancia_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='sustancia',
            name='user_updated',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_updated_representantetecnico_sustancia_set', to=settings.AUTH_USER_MODEL),
        ),
    ]
