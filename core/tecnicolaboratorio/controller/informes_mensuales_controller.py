import json

from django.apps import apps
from django.db import transaction
from django.db.models import Sum
from django.db.models.functions import Coalesce

from app.settings import MEDIA_URL
from core.base.decorators import get_model
from core.base.formaters import format_datetime
from core.base.mixins.controller import Controller


class InformesMensualesController(Controller):
    model_str = "representantetecnico.InformesMensuales"
    estados_limitantes = ['revision', 'registrado']

    def archivar_informe(self, request):
        self.validate_access(request)

        with transaction.atomic():
            estado_transaccion_model = apps.get_model("representantetecnico", "EstadoTransaccion")
            tipo_mov_inv_model = apps.get_model("representantetecnico", "TipoMovimientoInventario")
            inventario_model = apps.get_model("representantetecnico", "Inventario")

            estado_transaccion = estado_transaccion_model.objects.get(estado="archivado")
            tipo_movimiento_del = tipo_mov_inv_model.objects.get(nombre='delete')

            self.object.estado_informe_id = estado_transaccion.id
            self.object.save()

            for det in self.object.informesmensualesdetalle_set.all():
                cantidad_desglose = det.desgloseinfomemensualdetalle_set.all().aggregate(
                    cantidad=Coalesce(Sum("cantidad"), 0)).get('cantidad')

                if cantidad_desglose != det.cantidad:
                    raise Exception("La cantidad desglosada total del consumo no coincide con "
                                    "la cantidad descrita en el detalle del informe para la "
                                    "sustancia {}".format(det.stock.sustancia.nombre))
                stock = det.stock
                stock.cantidad = stock.cantidad - det.cantidad
                stock.save()

                inv = inventario_model()
                inv.informe_mensual_detalle_id = det.id
                inv.cantidad_movimiento = det.cantidad
                inv.tipo_movimiento_id = tipo_movimiento_del.id
                inv.save()

    def create_object(self, request):
        estado_transaccion_model = apps.get_model("representantetecnico", "EstadoTransaccion")
        informes_mens_det_model = apps.get_model("representantetecnico", "InformesMensualesDetalle")

        estado_transaccion = estado_transaccion_model.objects.get(estado="registrado")

        sustancias = json.loads(request.POST['sustancias'])

        current_lab_user = request.user.laboratorio_set.first()

        self.object.laboratorio_id = current_lab_user.id

        with transaction.atomic():

            if self.verify_month_exist_with_year(self.object.mes.id, self.object.year,
                                                 current_lab_user.id):
                raise Exception(
                    'Ya existe un informe registrado con este mes para este año con el '
                    'laboratorio {}'.format(self.object.laboratorio.nombre)
                )

            self.object.estado_informe_id = estado_transaccion.id
            self.object.save()

            for i in sustancias:
                det = informes_mens_det_model()
                det.stock_id = i['id']
                det.informe_id = self.object.id
                det.cantidad = float(i['cantidad_consumida'])
                det.save()

    def delete_object(self):
        if self.permit_delete() is False:
            raise Exception("No es posible eliminar este registro")

        self.object.delete()

    def get_doc_informe(self):
        if self.object.doc_informe:
            return '{}{}'.format(MEDIA_URL, self.object.doc_informe)
        return ''

    def get_informe_detail(self):
        data = []
        for i in self.object.informesmensualesdetalle_set.all():
            data.append({
                'id': i.id,
                'stock': {
                    'id': i.stock_id,
                    'nombre': i.stock.sustancia.nombre,
                    'unidad_medida': i.stock.sustancia.unidad_medida.nombre,
                    'cantidad_lab': i.stock.cantidad
                },
                'cantidad': i.cantidad
            })
        return data

    @get_model
    def get_years_in_stock(self):
        return self.model.objects.order_by('year').distinct("year").values('year')

    def permit_delete(self):
        if self.object.estado_informe is not None:
            if self.object.estado_informe.estado == "archivado":
                return False

        return True

    @get_model
    def search_data(self, type_data, id_data, request):
        query = None
        data = []
        current_lab_user = request.user.laboratorio_set.first()

        if type_data == 'year':
            if request.session['group'].name == 'laboratorio':
                query = self.model.objects.filter(year=id_data, laboratorio_id=current_lab_user.id)
            elif request.session['group'].name == 'representante':
                query = self.model.objects.filter(year=id_data)
        elif type_data == 'mes':
            if request.session['group'].name == 'laboratorio':
                query = self.model.objects.filter(mes_id=id_data, laboratorio_id=current_lab_user.id)
            elif request.session['group'].name == 'representante':
                query = self.model.objects.filter(mes_id=id_data)
        else:
            if request.session['group'].name == 'laboratorio':
                query = self.model.objects.filter(laboratorio_id=current_lab_user.id)
            elif request.session['group'].name == 'representante':
                query = self.model.objects.all()
        if query is not None:
            for i in query:
                item = {
                    'id': i.id,
                    'laboratorio': i.laboratorio.nombre,
                    'mes': i.mes.nombre,
                    'year': i.year,
                    'fecha_creat': format_datetime(i.date_creation, is_time=False),
                    'estado': i.estado_informe.estado
                }
                data.append(item)
        return data

    def update_object(self, request):
        estado_transaccion_model = apps.get_model("representantetecnico", "EstadoTransaccion")
        informes_mens_det_model = apps.get_model("representantetecnico", "InformesMensualesDetalle")

        self.verify_form_informe_updated()

        estadoinforme = estado_transaccion_model.objects.get(estado='registrado')

        detalle_informe_new = json.loads(request.POST['detalle_informe'])

        with transaction.atomic():

            if self.permit_delete() is False:
                raise Exception('No es posible actualizar este registro')

            self.object.estado_informe_id = estadoinforme.id
            self.object.save()

            detalle_informe_old = self.object.informesmensualesdetalle_set.all()

            for dc_old in detalle_informe_old:
                exits_old = False

                for dc_new in detalle_informe_new:
                    if dc_old.id == dc_new['id']:
                        exits_old = True
                        break

                if exits_old is False:
                    dc_old.delete()

            detalle_informe_old = self.object.informesmensualesdetalle_set.all()

            for dc_new in detalle_informe_new:
                exits_old = False
                item_det_new = None
                stock_new = dc_new['stock']

                for dc_old in detalle_informe_old:
                    if dc_old.id == dc_new['id']:
                        exits_old = True
                        item_det_new = dc_old
                        break

                if exits_old is False and item_det_new is None:
                    item_det_new = informes_mens_det_model()

                item_det_new.stock_id = stock_new['id']
                item_det_new.informe_id = self.object.id
                item_det_new.cantidad = float(dc_new['cantidad'])
                item_det_new.save()

    def validate_creation(self, current_user):
        estado_transaccion_model = apps.get_model("representantetecnico", "EstadoTransaccion")

        current_lab_user = current_user.laboratorio_set.first()

        estados = estado_transaccion_model.objects.filter(
            informesmensuales__estado_informe__estado__in=self.estados_limitantes,
            informesmensuales__laboratorio_id=current_lab_user.id)

        if estados.exists():
            return False
        return True

    def validate_access(self, request):
        if self.permit_delete() is False:
            raise Exception("No se puede realizar acciones sobre este registro")

        if request.session['group'].name != 'laboratorio':
            raise Exception('No tiene permiso para realiziar esta accion')

        current_lab_user = request.user.laboratorio_set.first()

        if self.object.laboratorio_id != current_lab_user.id:
            raise Exception('Este informe no pertenece a su laboratorio')

    @get_model
    def verify_form_informe_updated(self):

        informe_old = self.model.objects.get(pk=self.object.id)

        if informe_old.laboratorio_id != self.object.laboratorio_id:
            raise Exception('No se puede actualizar un laboratorio diferente')
        if informe_old.mes.id != self.object.mes.id:
            raise Exception("No se puede actualizar a un mes diferente")
        if informe_old.year != self.object.year:
            raise Exception("No se puede actualizar a un año diferente")

    @get_model
    def verify_month_exist_with_year(self, mes_id, year, laboratorio_id):
        if self.model.objects.filter(mes_id=mes_id, year=year, laboratorio_id=laboratorio_id).exists():
            return True

        return False
