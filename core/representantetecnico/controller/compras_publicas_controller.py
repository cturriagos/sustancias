from datetime import datetime

from django.apps import apps
from django.core.exceptions import PermissionDenied
from django.db import transaction

from app.settings import MEDIA_URL
from core.base import querysets
from core.base.decorators import get_model
from core.base.mixins.controller import Controller
from core.base.querysets import get_cupo_consumido


class ComprasPublicasController(Controller):
    model_str = "representantetecnico.ComprasPublicas"

    @get_model
    def actualizar_compra(self, detalle_compras_new):
        estado_transaccion_model = apps.get_model("representantetecnico", "EstadoTransaccion")
        comp_publ_det_model = apps.get_model("representantetecnico", "ComprasPublicasDetalle")

        estadocompra = estado_transaccion_model.objects.get(estado='registrado')
        if detalle_compras_new is not None:
            with transaction.atomic():
                if self.object.estado_compra.estado == 'almacenado':
                    raise Exception(
                        "Compra ya almacenada en stock, no se puede actualizar"
                    )
                self.object.estado_compra_id = estadocompra.id
                self.object.observacion = None
                self.object.save()
                detalle_compras_old = comp_publ_det_model.objects.filter(compra_id=self.object.id)

                for dc_old in detalle_compras_old:
                    exits_old = False
                    for dc_new in detalle_compras_new:
                        if dc_old.id == dc_new['id']:
                            exits_old = True
                            break
                    if exits_old is False:
                        dc_old.delete()

                detalle_compras_old = comp_publ_det_model.objects.filter(compra_id=self.object.id)

                for dc_new in detalle_compras_new:
                    exits_old = False
                    item_det_new = None
                    stock_old = dc_new['stock']

                    for dc_old in detalle_compras_old:
                        if dc_old.id == dc_new['id']:
                            exits_old = True
                            item_det_new = dc_old
                            break

                    if exits_old is False and item_det_new is None:
                        item_det_new = comp_publ_det_model()

                    item_det_new.stock_id = stock_old['id']
                    item_det_new.compra_id = self.object.id
                    item_det_new.cantidad = float(dc_new['cantidad'])
                    item_det_new.save()
        else:
            raise Exception('Faltan datos')

    def confirmar_compra(self, observacion):
        with transaction.atomic():
            estado_transaccion_model = apps.get_model("representantetecnico", "EstadoTransaccion")
            inventario_model = apps.get_model("representantetecnico", "Inventario")
            tipo_movimiento_model = apps.get_model("representantetecnico", "TipoMovimientoInventario")

            if self.object.estado_compra.estado == 'almacenado':
                raise Exception(
                    "Compra ya almacenada en stock, no se puede actualizar"
                )

            tipo_movimiento = tipo_movimiento_model.objects.get(nombre='add')
            compras_estado = estado_transaccion_model.objects.get(estado='almacenado')

            self.object.estado_compra_id = compras_estado.id
            if observacion is None:
                observacion = ""
            self.object.observacion = observacion
            self.object.save()

            for det in self.object.compraspublicasdetalle_set.all():
                # verificar si existe cupo para entregar la sustancia
                cupo_consumido = get_cupo_consumido(datetime.now().year, det.stock.sustancia_id)
                cupo_autorizado = float(det.stock.sustancia.cupo_autorizado)

                if cupo_consumido + float(det.cantidad) > cupo_autorizado:
                    raise PermissionDenied(
                        'La sustancia {} sobrepasa el cupo autorizado, verifique'.format(
                            det.stock.sustancia.nombre)
                    )

                stock = det.stock
                stock.cantidad = stock.cantidad + det.cantidad
                stock.save()

                inv = inventario_model()
                inv.compra_publica_detalle_id = det.id
                inv.cantidad_movimiento = det.cantidad
                inv.tipo_movimiento_id = tipo_movimiento.id
                inv.save()

    @get_model
    def delete_object(self):
        if self.permit_delete() is False:
            raise Exception(
                "Compra ya almacenada en stock, no se puede eliminar"
            )
        self.object.delete()

    @get_model
    def get_convocatorias_compra(self):
        return self.model.objects.order_by('convocatoria').distinct('convocatoria').values("convocatoria")

    @get_model
    def get_factura(self):
        if self.object.factura:
            return '{}{}'.format(MEDIA_URL, self.object.factura)
        return ''

    def get_guia_transporte(self):
        if self.object.guia_transporte:
            return '{}{}'.format(MEDIA_URL, self.object.guia_transporte)
        return ''

    def get_observacion(self):
        if self.object.observacion:
            return self.object.observacion
        return ""

    def get_pedido_compras_publicas(self):
        if self.object.pedido_compras_publicas:
            return '{}{}'.format(MEDIA_URL, self.object.pedido_compras_publicas)
        return ''

    def permit_delete(self):
        if self.object.estado_compra.estado == 'almacenado':
            return False
        return True

    def registrar_compra(self, sustancias):
        with transaction.atomic():
            estado_transaccion_model = apps.get_model("representantetecnico", "EstadoTransaccion")
            comp_publ_det_model = apps.get_model("representantetecnico", "ComprasPublicasDetalle")

            estadocompra = estado_transaccion_model.objects.get(estado='registrado')

            self.object.estado_compra_id = estadocompra.id
            self.object.save()

            for i in sustancias:
                det = comp_publ_det_model()
                det.stock_id = i['id']
                det.compra_id = self.object.id
                det.cantidad = float(i['cantidad_ingreso'])
                det.save()

    def revision_compra(self, observacion):
        with transaction.atomic():
            estado_transaccion_model = apps.get_model("representantetecnico", "EstadoTransaccion")

            if self.object.estado_compra.estado == 'almacenado':
                raise Exception(
                    "Compra ya almacenada en stock, no se puede actualizar"
                )
            compras_estado = estado_transaccion_model.objects.get(estado='revision')
            self.object.estado_compra_id = compras_estado.id
            if observacion is None:
                observacion = ""
            self.object.observacion = observacion
            self.object.save()

    @get_model
    def search_data(self, type_filter, id_s, request):
        data = []
        if type_filter == 'est':
            if request.session['group'].name == 'bodega':
                query = self.model.objects.filter(estado_compra_id=id_s, bodega__responsable_id=request.user.id)
            else:
                query = self.model.objects.filter(estado_compra_id=id_s)
        elif type_filter == 'conv':
            if request.session['group'].name == 'bodega':
                query = self.model.objects.filter(convocatoria=id_s, bodega__responsable_id=request.user.id)
            else:
                query = self.model.objects.filter(convocatoria=id_s)
        elif type_filter == 'emp':
            if request.session['group'].name == 'bodega':
                query = self.model.objects.filter(empresa_id=id_s, bodega__responsable_id=request.user.id)
            else:
                query = self.model.objects.filter(empresa_id=id_s)
        else:
            if request.session['group'].name == 'bodega':
                query = self.model.objects.filter(bodega__responsable_id=request.user.id)
            else:
                query = self.model.objects.all()

        for i in query:
            item = {'id': i.id, 'llegada_bodega': i.llegada_bodega,
                    'hora_llegada_bodega': i.hora_llegada_bodega,
                    'convocatoria': i.convocatoria, 'estado': i.estado_compra.estado,
                    'empresa': i.empresa.nombre}
            data.append(item)
        return data

    def search_detail(self):
        data = []
        for dci in self.object.compraspublicasdetalle_set.all():
            item = {'id': dci.id, 'cantidad': float(dci.cantidad),
                    'bodega_selected': {'id': dci.stock.bodega.id, 'text': dci.stock.bodega.nombre},
                    'stock': {'id': dci.stock.id,
                              'cupo_autorizado': float(dci.stock.sustancia.cupo_autorizado),
                              'value': dci.stock.sustancia.nombre,
                              'unidad_medida': dci.stock.sustancia.unidad_medida.nombre,
                              'cantidad_bodega': float(dci.stock.cantidad),
                              'cupo_consumido': querysets.get_cupo_consumido(datetime.now().year,
                                                                             dci.stock.sustancia_id)
                              }
                    }
            data.append(item)
        return data
