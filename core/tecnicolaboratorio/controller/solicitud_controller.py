import json
from datetime import datetime

from django.apps import apps
from django.core.exceptions import PermissionDenied
from django.db import transaction

from app.settings import MEDIA_URL
from core.base import querysets
from core.base.decorators import get_model
from core.base.mixins.controller import Controller


class SolicitudController(Controller):
    model_str = "representantetecnico.Solicitud"
    estados_editables = ['revision', 'registrado']
    estados_no_editables = ['almacenado', 'entregado', 'aprobado', 'recibido', 'archivado']

    def aprobar_solicitud(self, tipoobs, observacion):
        if tipoobs is None:
            raise Exception('Faltan datos')

        with transaction.atomic():
            estado_transaccion_model = apps.get_model("representantetecnico", "EstadoTransaccion")

            estado_solicitud = estado_transaccion_model.objects.get(estado='aprobado')

            if observacion is None:
                observacion = ""

            if tipoobs == "rp":
                self.object.observacion_representante = observacion
            elif tipoobs == "bdg":
                self.object.observacion_bodega = observacion

            self.object.estado_solicitud_id = estado_solicitud.id
            self.object.fecha_autorizacion = datetime.now()
            self.object.save()

    def create_object(self, request):

        sustancias = json.loads(request.POST['sustancias'])

        estado_transaccion_model = apps.get_model("representantetecnico", "EstadoTransaccion")
        solicitud_detalle_model = apps.get_model("representantetecnico", "SolicitudDetalle")

        estadosolicitud = estado_transaccion_model.objects.get(estado='registrado')

        with transaction.atomic():
            current_lab_user = request.user.laboratorio_set.first()

            self.object.estado_solicitud_id = estadosolicitud.id
            self.object.laboratorio_id = current_lab_user.id

            self.object.save()

            for i in sustancias:
                det = solicitud_detalle_model()

                det.sustancia_id = i['id']
                det.solicitud_id = self.object.id
                det.cantidad_solicitada = float(i['cantidad_solicitud'])

                det.save()

    def delete_object(self):
        if self.permit_delete() is False:
            raise Exception('No es posible eliminar este registro')

        self.object.delete()

    def entregar_solicitud(self, detalle_solicitud, observacion_solicitud):
        if detalle_solicitud is None or observacion_solicitud is None:
            raise Exception("Faltan datos")

        with transaction.atomic():
            estado_transaccion_model = apps.get_model("representantetecnico", "EstadoTransaccion")
            tipo_mov_inv_model = apps.get_model("representantetecnico", "TipoMovimientoInventario")
            stock_model = apps.get_model("representantetecnico", "Stock")
            inventario_model = apps.get_model("representantetecnico", "Inventario")

            detalle_solicitud = json.loads(detalle_solicitud)

            tipo_movimiento_del = tipo_mov_inv_model.objects.get(nombre='delete')
            tipo_movimiento_add = tipo_mov_inv_model.objects.get(nombre='add')

            estado_solicitud = estado_transaccion_model.objects.get(estado='entregado')

            self.object.estado_solicitud_id = estado_solicitud.id
            self.object.observacion_bodega = observacion_solicitud
            self.object.save()

            for i in self.object.solicituddetalle_set.all():
                # actualiza la cantidad a entregar
                for ds_new in detalle_solicitud:
                    if ds_new['id'] == i.id:
                        i.cantidad_entregada = float(ds_new['cant_ent'])
                        break

                i.save()

                # verificar si existe cupo para entregar la sustancia
                cupo_consumido = querysets.get_cupo_consumido(datetime.now().year, i.sustancia_id)
                cupo_autorizado = float(i.sustancia.cupo_autorizado)

                if cupo_consumido + float(i.cantidad_entregada) > cupo_autorizado:
                    raise PermissionDenied(
                        'La sustancia {} sobrepasa el cupo permitido, verifique'.format(
                            i.sustancia.nombre)
                    )

                # disminuye stock en bodega
                stockbdg = stock_model.objects.get(sustancia_id=i.sustancia.id,
                                                   bodega_id=i.solicitud.bodega.id)
                stockbdg.cantidad = float(stockbdg.cantidad) - i.cantidad_entregada
                stockbdg.save()

                # movimiento de inventario delete de bodega
                inv = inventario_model()
                inv.solicitud_detalle_id = i.id
                inv.cantidad_movimiento = i.cantidad_entregada
                inv.tipo_movimiento_id = tipo_movimiento_del.id
                inv.save()

                # Aumenta el stock de el laboratorio
                stocklab = stock_model.objects.get(laboratorio_id=i.solicitud.laboratorio.id,
                                                   sustancia_id=i.sustancia.id)
                stocklab.cantidad = float(stocklab.cantidad) + i.cantidad_entregada
                stocklab.save()

                # movimiento de inventario addsustancialab en el laboratorio
                invlab = inventario_model()
                invlab.solicitud_detalle_id = i.id
                invlab.cantidad_movimiento = i.cantidad_entregada
                invlab.tipo_movimiento_id = tipo_movimiento_add.id
                invlab.save()

    def get_doc_solicitud(self):
        if self.object.documento_solicitud:
            return '{}{}'.format(MEDIA_URL, self.object.documento_solicitud)
        return ''

    def get_estados_editables(self):
        return self.estados_editables

    def get_fecha_autorizacion(self):
        if self.object.fecha_autorizacion is not None:
            return self.object.fecha_autorizacion.strftime("%Y-%m-%d %H:%M:%S")
        return ''

    def permit_delete(self):
        if self.object.estado_solicitud is not None:
            if self.object.estado_solicitud.estado in self.estados_no_editables:
                return False

        return True

    def recibir_solicitud(self):
        with transaction.atomic():
            estado_transaccion_model = apps.get_model("representantetecnico", "EstadoTransaccion")

            estado_solicitud = estado_transaccion_model.objects.get(estado='recibido')

            self.object.estado_solicitud_id = estado_solicitud.id
            self.object.save()

    def revision_solicitud(self, tipoobs, observacion):
        if tipoobs is None:
            raise Exception('Faltan datos')

        with transaction.atomic():

            if self.permit_delete() is False:
                if tipoobs == 'bdg' and self.object.estado_solicitud.estado != 'aprobado':
                    raise Exception("No es posible manipular este registro este registro")

            estado_transaccion_model = apps.get_model("representantetecnico", "EstadoTransaccion")

            estado_solicitud = estado_transaccion_model.objects.get(estado='revision')

            if observacion is None:
                observacion = ""

            if tipoobs == "rp":
                self.object.observacion_representante = observacion
            elif tipoobs == "bdg":
                self.object.observacion_bodega = observacion

            self.object.estado_solicitud_id = estado_solicitud.id
            self.object.fecha_autorizacion = None
            self.object.save()

    @get_model
    def search_data(self, type_data, id_data, request):
        data = []
        if type_data == 'lab':
            if request.session['group'].name == 'laboratorio':
                query = self.model.objects.all().filter(laboratorio_id=id_data,
                                                        laboratorio__responsable_id=request.user.id)
            elif request.session['group'].name == 'bodega':
                query = self.model.objects.all().filter(laboratorio_id=id_data,
                                                        bodega__responsable_id=request.user.id)
            else:
                query = self.model.objects.all().filter(laboratorio_id=id_data)
        elif type_data == 'est':
            if request.session['group'].name == 'bodega':
                query = self.model.objects.all().filter(estado_solicitud_id=id_data,
                                                        bodega__responsable_id=request.user.id)
            elif request.session['group'].name == 'laboratorio':
                query = self.model.objects.all().filter(estado_solicitud_id=id_data,
                                                        laboratorio__responsable_id=request.user.id)
            else:
                query = self.model.objects.all().filter(estado_solicitud_id=id_data)
        else:
            if request.session['group'].name == 'bodega':
                query = self.model.objects.filter(bodega__responsable_id=request.user.id)
            elif request.session['group'].name == 'laboratorio':
                query = self.model.objects.filter(laboratorio__responsable_id=request.user.id)
            else:
                query = self.model.objects.all()
        for solicitud in query:
            item = {
                'id': solicitud.id,
                'codigo': solicitud.codigo_solicitud,
                'proy': "",
                'fe_aut': solicitud.controller.get_fecha_autorizacion(),
                'est': solicitud.estado_solicitud.estado,
            }

            if request.session['group'].name != 'laboratorio':
                item['lab'] = solicitud.laboratorio.nombre

            if solicitud.proyecto is not None:
                item['proy'] = solicitud.proyecto.nombre

            data.append(item)

        return data

    def search_detail(self):
        data = []

        for dci in self.object.solicituddetalle_set.all():
            item = {
                'id': dci.id,
                'cantidad_solicitud': dci.cantidad_solicitada,
                'bodega_selected': {'id': dci.solicitud.bodega.id, 'text': dci.solicitud.bodega.nombre},
                'sustancia': {
                    'id': dci.sustancia.id,
                    'cupo_autorizado': dci.sustancia.cupo_autorizado,
                    'value': dci.sustancia.nombre,
                    'unidad_medida': dci.sustancia.unidad_medida.nombre,
                    'cantidad_bodega': dci.sustancia.stock_set.get(
                        bodega_id=dci.solicitud.bodega_id).cantidad
                }
            }

            data.append(item)

        return data

    def search_detalle(self):
        data = []

        for i in self.object.solicituddetalle_set.all():
            data.append({
                'id': i.id,
                'sustancia': i.sustancia.nombre,
                'cant_bdg': float(i.sustancia.stock_set.get(bodega_id=i.solicitud.bodega.id).cantidad),
                'cant_sol': float(i.cantidad_solicitada),
                'cant_ent': float(i.cantidad_entregada)
            })

        return data

    @get_model
    def search_detalle_sin_sesion(self, solicitud_id):
        self.object = self.model.objects.get(pk=solicitud_id)
        return self.search_detalle()

    def search_sol_rec(self, id_stock, det_inf, request):
        estado_transaccion_model = apps.get_model("representantetecnico", "EstadoTransaccion")
        solicitud_detalle_model = apps.get_model("representantetecnico", "SolicitudDetalle")

        current_lab_user = request.user.laboratorio_set.first()

        data = [{'id': '', 'text': '---------'}]
        estado_solicitud = estado_transaccion_model.objects.get(estado="recibido")

        for i in solicitud_detalle_model.objects.filter(sustancia__stock__id=id_stock,
                                                        solicitud__laboratorio_id=current_lab_user.id,
                                                        solicitud__user_creation_id=request.user.id,
                                                        solicitud__estado_solicitud_id=estado_solicitud.id) \
                .exclude(desgloseinfomemensualdetalle__informe_mensual_detalle_id=det_inf):
            item = {'id': i.id, 'cantidad_solicitada': float(i.cantidad_solicitada),
                    'cantidad_entregada': float(i.cantidad_entregada),
                    'text': "{} {}".format(i.solicitud.codigo_solicitud, i.solicitud.proyecto.__str__()),
                    'consumidor': i.solicitud.proyecto.responsable.__str__()}
            data.append(item)
        return data

    def update_object(self, request):
        with transaction.atomic():
            estado_transaccion_model = apps.get_model("representantetecnico", "EstadoTransaccion")
            solicitud_detalle_model = apps.get_model("representantetecnico", "SolicitudDetalle")

            estadosolicitud = estado_transaccion_model.objects.get(estado='registrado')

            detalle_solicitud_new = json.loads(request.POST['detalle_solicitud'])

            if self.permit_delete() is False:
                raise Exception("No es posible actualizar este registro")

            self.object.estado_solicitud_id = estadosolicitud.id
            self.object.observacion_bodega = None
            self.object.observacion_representante = None
            self.object.fecha_autorizacion = None
            self.object.save()

            detalle_solicitud_old = solicitud_detalle_model.objects.filter(solicitud_id=self.object.id)

            for dc_old in detalle_solicitud_old:
                exits_old = False

                for dc_new in detalle_solicitud_new:
                    if dc_old.id == dc_new['id']:
                        exits_old = True
                        break

                if exits_old is False:
                    dc_old.delete()

            detalle_solicitud_old = solicitud_detalle_model.objects.filter(solicitud_id=self.object.id)

            for dc_new in detalle_solicitud_new:
                exits_old = False
                item_det_new = None
                sustancia_new = dc_new['sustancia']

                for dc_old in detalle_solicitud_old:
                    if dc_old.id == dc_new['id']:
                        exits_old = True
                        item_det_new = dc_old
                        break

                if exits_old is False and item_det_new is None:
                    item_det_new = solicitud_detalle_model()

                item_det_new.sustancia_id = sustancia_new['id']
                item_det_new.solicitud_id = self.object.id
                item_det_new.cantidad_solicitada = float(dc_new['cantidad_solicitud'])
                item_det_new.save()
