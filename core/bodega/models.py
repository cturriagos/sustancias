from django.db import models

from core.base.models import BaseModel
from core.bodega.controller.bodega_controller import BodegaController


class Bodega(BaseModel):
    nombre = models.CharField(max_length=20, verbose_name="Nombre", unique=True)
    descripcion = models.CharField(max_length=200, verbose_name="Descripción", blank=True, null=True)
    direccion = models.CharField(max_length=200, verbose_name="Direccion", blank=True, null=True)
    responsable = models.ForeignKey("login.User", on_delete=models.SET_NULL, verbose_name="Responsable",
                                    null=True, blank=True)

    controller = BodegaController()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller.object = self

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Bodega"
        verbose_name_plural = "Bodegas"
        db_table = "bodega"
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(fields=['responsable'], name="Unico reponsable con unica bodega")
        ]
