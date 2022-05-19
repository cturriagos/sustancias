from datetime import datetime

from django.db import models

from core.base.models import BaseModel
from core.tecnicolaboratorio.controller.laboratorio_controller import LaboratorioController
from core.tecnicolaboratorio.controller.proyecto_controller import ProyectoController


class Laboratorio(BaseModel):
    nombre = models.CharField(max_length=100, verbose_name="Nombre de laboratorio", unique=True)
    direccion = models.CharField(max_length=300, null=True, blank=True, verbose_name="Dirección")
    responsable = models.ForeignKey("login.User", verbose_name="Responsable", on_delete=models.SET_NULL, null=True,
                                    blank=True)

    controller = LaboratorioController()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = LaboratorioController(instance=self)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Laboratorio"
        verbose_name_plural = "Laboratorios"
        db_table = "laboratorio"
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(fields=['responsable'], name="Unico reponsable con unico laboratorio")
        ]


class Proyecto(BaseModel):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    descripcion = models.CharField(max_length=500, verbose_name="Descripcion", null=True, blank=True)
    tipo_actividad = models.ForeignKey("representantetecnico.TipoActividad", on_delete=models.RESTRICT,
                                       verbose_name="Tipo de proyecto", null=True)
    laboratorio = models.ForeignKey("tecnicolaboratorio.Laboratorio", on_delete=models.RESTRICT,
                                    verbose_name="Laboratorio")
    responsable = models.ForeignKey("login.User", verbose_name="Responsable", on_delete=models.RESTRICT, null=True)
    fecha_inicio = models.DateTimeField(default=datetime.now, null=True, blank=True)
    fecha_fin = models.DateTimeField(default=datetime.now, null=True, blank=True)

    controller = ProyectoController()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = ProyectoController(instance=self)

    def __str__(self):
        return self.nombre or ""

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"
        db_table = "proyecto"
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(fields=['nombre', 'laboratorio'], name="Unico proyecto por laboratorio")
        ]
