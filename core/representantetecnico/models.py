from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

from core.base.models import BaseModel
from core.representantetecnico.controller.compras_publicas_controller import ComprasPublicasController
from core.representantetecnico.controller.empresa_controller import EmpresaController
from core.representantetecnico.controller.inventario_controller import InventarioController
from core.representantetecnico.controller.repositorio_controller import RepositorioController
from core.bodega.controller.sustancia_controller import SustanciaController
from core.representantetecnico.validators import validate_compras_convocatoria
from core.tecnicolaboratorio.controller.desglose_infome_mensual_detalle_controller import \
    DesgloseInfomeMensualDetalleController
from core.tecnicolaboratorio.controller.informes_mensuales_controller import InformesMensualesController
from core.tecnicolaboratorio.controller.solicitud_controller import SolicitudController


class TipoActividad(models.Model):
    nombre = models.CharField(max_length=20, verbose_name="Nombre", unique=True)
    descripcion = models.CharField(max_length=200, blank=True, null=True, verbose_name="Descripcion")
    is_active = models.BooleanField(default=True, editable=False)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Tipo de actividad"
        verbose_name_plural = "Tipos de actividades"
        db_table = "tipo_actividad"
        ordering = ["id"]


class EstadoTransaccion(models.Model):
    estado = models.CharField(max_length=100, verbose_name="Estado", unique=True)
    descripcion = models.CharField(max_length=300, verbose_name="Descripcion", null=True, blank=True)
    is_active = models.BooleanField(default=True, editable=False)

    def __str__(self):
        return str(self.estado)

    class Meta:
        verbose_name = "Estado de transacción"
        verbose_name_plural = "Estado de transacciones"
        db_table = "estado_transaccion"
        ordering = ["id"]


class UnidadMedida(models.Model):
    nombre = models.CharField(max_length=20, verbose_name="Nombre de unidad de medida", unique=True)
    simbolo = models.CharField(max_length=5, verbose_name="Simbolo de la unidad de medida", null=True)
    descripcion = models.CharField(max_length=200, verbose_name="Descripción", blank=True,
                                   null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Unidad de medida"
        verbose_name_plural = "Unidades de medida"
        db_table = "unidad_medida"
        ordering = ["id"]


class Sustancia(BaseModel):
    nombre = models.CharField(max_length=100, verbose_name="Nombre de sustancia", unique=True)
    unidad_medida = models.ForeignKey("representantetecnico.UnidadMedida", on_delete=models.PROTECT,
                                      verbose_name="Unidad de medida", null=True)
    descripcion = models.CharField(max_length=200, verbose_name="Descripción de la sustancia", blank=True,
                                   null=True)
    cupo_autorizado = models.DecimalField(default=0, verbose_name="Cupo autorizado", max_digits=9,
                                          decimal_places=4)

    controller = SustanciaController()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = SustanciaController(instance=self)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Sustancia"
        verbose_name_plural = "Sustancias"
        db_table = "sustancia"
        ordering = ["id"]


class Stock(BaseModel):
    sustancia = models.ForeignKey("representantetecnico.Sustancia", on_delete=models.CASCADE, null=True)
    bodega = models.ForeignKey("bodega.Bodega", on_delete=models.PROTECT, null=True)
    laboratorio = models.ForeignKey("tecnicolaboratorio.Laboratorio", on_delete=models.PROTECT, null=True)
    cantidad = models.DecimalField(max_digits=9, decimal_places=4, default=0)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Stock sustancia"
        verbose_name_plural = "Stock sustancias"
        db_table = "stock"
        ordering = ["id"]


class Solicitud(BaseModel):
    laboratorio = models.ForeignKey("tecnicolaboratorio.Laboratorio", on_delete=models.PROTECT,
                                    verbose_name="Laboratorio", null=True)
    bodega = models.ForeignKey("bodega.Bodega", on_delete=models.PROTECT, verbose_name="Bodega", null=True)
    proyecto = models.ForeignKey("tecnicolaboratorio.Proyecto", null=True, on_delete=models.PROTECT,
                                 verbose_name="Proyecto")
    documento_solicitud = models.FileField(upload_to='solicitud/%Y/%m/%d', null=True)
    codigo_solicitud = models.CharField(max_length=50, verbose_name="Codigo de solicitud", null=True)
    fecha_autorizacion = models.DateTimeField(editable=False, null=True)
    estado_solicitud = models.ForeignKey("representantetecnico.EstadoTransaccion", on_delete=models.PROTECT,
                                         verbose_name="Estados solicitud", null=True)
    observacion_representante = models.TextField(verbose_name="Observación", null=True, blank=True)
    observacion_bodega = models.TextField(verbose_name="Observación", null=True, blank=True)

    controller = SolicitudController()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = SolicitudController(instance=self)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Solicitud"
        verbose_name_plural = "Solicitudes"
        db_table = "solicitud"
        ordering = ["id"]


class SolicitudDetalle(BaseModel):
    solicitud = models.ForeignKey("representantetecnico.Solicitud", on_delete=models.CASCADE, verbose_name="Solicitud")
    sustancia = models.ForeignKey("representantetecnico.Sustancia", on_delete=models.PROTECT, verbose_name="Sustancia",
                                  null=True)
    cantidad_solicitada = models.DecimalField(verbose_name="Cantidad solicitada", decimal_places=4, max_digits=8,
                                              null=True, default=0)
    cantidad_entregada = models.DecimalField(verbose_name="Cantidad entregada", decimal_places=4, max_digits=8,
                                             null=True, default=0)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Solicitud Detalle"
        verbose_name_plural = "Solicitud Detalles"
        db_table = "detalle_solicitud"
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(fields=['solicitud', 'sustancia'], name="Unica sustancia por laboratorio")
        ]


class Proveedor(BaseModel):
    nombre = models.CharField(max_length=150, verbose_name="Nombre de empresa", unique=True)
    ruc = models.CharField(max_length=13, verbose_name="Ruc", unique=True)
    is_active = models.BooleanField(default=True, editable=False)

    controller = EmpresaController()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = EmpresaController(instance=self)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        db_table = "proveedor"
        ordering = ["id"]


class ComprasPublicas(BaseModel):
    empresa = models.ForeignKey("representantetecnico.Proveedor", on_delete=models.PROTECT, verbose_name="Empresa",
                                null=True)
    bodega = models.ForeignKey("bodega.Bodega", on_delete=models.PROTECT, verbose_name="Bodega", null=True)
    llegada_bodega = models.DateField(default=datetime.now, verbose_name="Fecha llegada a bodega")
    hora_llegada_bodega = models.TimeField(default=datetime.now, verbose_name="Hora llegada a bodega")
    convocatoria = models.IntegerField(blank=True, null=True, validators=[validate_compras_convocatoria])
    pedido_compras_publicas = models.FileField(upload_to='compras_publicas/%Y/%m/%d', null=True)
    guia_transporte = models.FileField(upload_to='compras_publicas/%Y/%m/%d', null=True)
    factura = models.FileField(upload_to='compras_publicas/%Y/%m/%d', null=True)
    estado_compra = models.ForeignKey("representantetecnico.EstadoTransaccion", on_delete=models.PROTECT,
                                      verbose_name="Estado de compras",
                                      null=True)
    observacion = models.TextField(verbose_name="Observación", null=True, blank=True, default="")

    controller = ComprasPublicasController()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = ComprasPublicasController(instance=self)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Compra Publica"
        verbose_name_plural = "Compras Publicas"
        db_table = "compras_publicas"
        ordering = ["id"]


class ComprasPublicasDetalle(BaseModel):
    compra = models.ForeignKey("representantetecnico.ComprasPublicas", on_delete=models.CASCADE, verbose_name="Compra")
    stock = models.ForeignKey(Stock, on_delete=models.PROTECT, verbose_name="Stock", null=True)
    cantidad = models.DecimalField(verbose_name="cantidad", decimal_places=4, max_digits=8, null=True, default=0)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Compra Publica Detalle"
        verbose_name_plural = "Compras Publicas Detalles"
        db_table = "detalle_compra_publica"
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(fields=['compra', 'stock'], name="Unico stock de sustancia por compra")
        ]


class Mes(models.Model):
    nombre = models.CharField(max_length=20, verbose_name="Nombre del mes", unique=True)
    numero = models.IntegerField(verbose_name="Numero de mes", unique=True)

    def __str__(self):
        return str(self.nombre)

    class Meta:
        verbose_name = "Mes"
        verbose_name_plural = "Meses"
        db_table = "mes"
        ordering = ["id"]


class InformesMensuales(BaseModel):
    laboratorio = models.ForeignKey("tecnicolaboratorio.Laboratorio", on_delete=models.PROTECT,
                                    verbose_name="Laboratorio")
    mes = models.ForeignKey("representantetecnico.Mes", on_delete=models.PROTECT, verbose_name="Mes", null=True)
    year = models.IntegerField(default=datetime.now().year, verbose_name="Año")
    doc_informe = models.FileField(upload_to='informemensual/%Y/%m/%d', null=True)
    estado_informe = models.ForeignKey("representantetecnico.EstadoTransaccion", on_delete=models.PROTECT, null=True,
                                       editable=False)

    controller = InformesMensualesController()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = InformesMensualesController(instance=self)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Informe mensual"
        verbose_name_plural = "Informes mensuales"
        db_table = "informes_mensuales"
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(fields=['laboratorio', 'mes', 'year'],
                                    name="Unica informe por mes y año en un laboratorio")
        ]


class InformesMensualesDetalle(BaseModel):
    informe = models.ForeignKey(InformesMensuales, on_delete=models.CASCADE, verbose_name="Informe")
    stock = models.ForeignKey(Stock, on_delete=models.PROTECT, verbose_name="Stock", null=True)
    cantidad = models.DecimalField(verbose_name="cantidad", decimal_places=4, max_digits=8, null=True, default=0)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Informe mensual Detalle"
        verbose_name_plural = "Informes mensuales Detalles"
        db_table = "detalle_informe_mensual"
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(fields=['informe', 'stock'], name="Unico stock de sustancia por informe")
        ]


class DesgloseInfomeMensualDetalle(BaseModel):
    informe_mensual_detalle = models.ForeignKey("representantetecnico.InformesMensualesDetalle",
                                                on_delete=models.CASCADE, null=True)
    documento = models.FileField(upload_to='informemensual/sustancias/desglose/%Y/%m/%d', null=True, blank=True)
    proyecto = models.ForeignKey("tecnicolaboratorio.Proyecto", null=True, on_delete=models.PROTECT,
                                 verbose_name="Proyecto")
    cantidad = models.DecimalField(verbose_name="cantidad", decimal_places=4, max_digits=8, null=True, default=0)

    controller = DesgloseInfomeMensualDetalleController()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = DesgloseInfomeMensualDetalleController(instance=self)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Desglose mensual"
        verbose_name_plural = "Desgloses mesuales"
        db_table = "desglose_detalle_informe_mensual"
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(fields=['informe_mensual_detalle', 'proyecto'],
                                    name="Unico proyecto por cada detalle de informe")
        ]


class TipoMovimientoInventario(models.Model):
    nombre = models.CharField(max_length=20, verbose_name="Nombre", unique=True)
    descripcion = models.CharField(max_length=200, verbose_name="Descripcion", blank=True, null=True)

    def __str__(self):
        return str(self.nombre)

    class Meta:
        verbose_name = "Tipo de movimiento de inventario"
        verbose_name_plural = "Tipos de movimientos de inventario"
        db_table = "tipo_movimiento_inventario"
        ordering = ["id"]


class Inventario(BaseModel):
    solicitud_detalle = models.ForeignKey("representantetecnico.SolicitudDetalle", on_delete=models.PROTECT, null=True)
    informe_mensual_detalle = models.ForeignKey("representantetecnico.InformesMensualesDetalle",
                                                on_delete=models.PROTECT, null=True)
    compra_publica_detalle = models.ForeignKey("representantetecnico.ComprasPublicasDetalle", on_delete=models.PROTECT,
                                               null=True)
    stock = models.ForeignKey("representantetecnico.Stock", on_delete=models.CASCADE, null=True)
    cantidad_movimiento = models.DecimalField(default=0, verbose_name="Cantidad movimiento", max_digits=9,
                                              decimal_places=4)
    tipo_movimiento = models.ForeignKey("representantetecnico.TipoMovimientoInventario", on_delete=models.PROTECT,
                                        verbose_name="Tipo de movimiento de inventario", null=True)

    controller = InventarioController()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = InventarioController(instance=self)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Inventario"
        verbose_name_plural = "Inventarios"
        db_table = "inventario"
        ordering = ["id"]


class TipoRepositorio(models.Model):
    nombre = models.CharField(max_length=20, verbose_name="Nombre", unique=True)
    descripcion = models.CharField(max_length=200, verbose_name="Descripcion", blank=True, null=True)

    def __str__(self):
        return str(self.nombre)

    class Meta:
        verbose_name = "Tipo de repositorio"
        verbose_name_plural = "Tipos de repositorios"
        db_table = "tipo_repositorio"
        ordering = ["id"]


class Repositorio(BaseModel):
    nombre = models.CharField(max_length=500, verbose_name="Nombre", null=True, blank=True)
    documento = models.FileField(upload_to='repositorio/%Y/%m/%d', null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    tipo_repositorio = models.ForeignKey('representantetecnico.TipoRepositorio', on_delete=models.RESTRICT, null=True)
    is_recicle_bin = models.BooleanField(default=False)
    is_file = models.BooleanField(default=False)
    is_dir = models.BooleanField(default=False)

    controller = RepositorioController()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = RepositorioController(instance=self)

    def __str__(self):
        return str(self.nombre)

    class Meta:
        verbose_name = "Repositorio"
        verbose_name_plural = "Repositorios"
        db_table = "repositorio"
        ordering = ["id"]
