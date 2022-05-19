from datetime import datetime

from django.apps import apps
from django.db import transaction

from core.base import querysets
from core.base.decorators import get_model
from core.base.mixins.controller import Controller


class SustanciaController(Controller):
    model_str = "representantetecnico.Sustancia"

    def _add_stock(self, stock_new):
        stock_model = apps.get_model("representantetecnico", "Stock")
        tipo_mov_inv_model = apps.get_model("representantetecnico", "TipoMovimientoInventario")
        inventario_model = apps.get_model("representantetecnico", "Inventario")

        tipo_movimiento_add = tipo_mov_inv_model.objects.get(nombre='add')

        stock = stock_model()
        stock.sustancia_id = self.object.id

        if stock_new['tipo'] == 'bodega':
            stock.bodega_id = stock_new['id_lugar']
        elif stock_new['tipo'] == 'laboratorio':
            stock.laboratorio_id = stock_new['id_lugar']

        stock.cantidad = float(stock_new['cantidad_ingreso'])
        stock.save()

        inv = inventario_model()
        inv.stock_id = stock.id
        inv.cantidad_movimiento = stock.cantidad
        inv.tipo_movimiento_id = tipo_movimiento_add.id
        inv.save()

    def crear_sustancia(self, lugares):
        with transaction.atomic():
            self.object.save()

            for i in lugares:
                self._add_stock(i)

    def delete_object(self):
        if self.permit_delete() is False:
            raise Exception(
                "No es posible eliminar este registro"
            )
        self.object.delete()

    def get_description(self):
        if self.object.descripcion:
            return self.object.descripcion
        return ""

    def _is_del(self):
        result = True
        if self.object.solicituddetalle_set.all().count() > 0:
            return False

        for st in self.object.stock_set.all():
            if st.compraspublicasdetalle_set.all().count() > 0 \
                    or st.informesmensualesdetalle_set.all().count() > 0:
                result = False
                break

        return result

    @get_model
    def list_desglose(self):
        stock_model = apps.get_model("representantetecnico", "Stock")
        bodega_model = apps.get_model("bodega", "Bodega")
        laboratorio_model = apps.get_model("tecnicolaboratorio", "Laboratorio")

        data = []
        for i in stock_model.objects.filter(sustancia_id=self.object.id, laboratorio=None).order_by(
                "bodega__nombre"):
            data.append({'id': i.id, 'nombre': i.bodega.nombre, 'tipo': 'bodega',
                         'cantidad_ingreso': float(i.cantidad)})
        for i in stock_model.objects.filter(sustancia_id=self.object.id, bodega=None).order_by(
                "laboratorio__nombre"):
            data.append({'id': i.id, 'nombre': i.laboratorio.nombre, 'tipo': 'laboratorio',
                         'cantidad_ingreso': float(i.cantidad)})
        for i in bodega_model.objects.exclude(stock__sustancia_id=self.object.id).order_by('nombre'):
            data.append({'id': -1, 'id_lugar': i.id, 'nombre': i.nombre, 'tipo': 'bodega',
                         'cantidad_ingreso': 0.0000})
        for i in laboratorio_model.objects.exclude(stock__sustancia_id=self.object.id).order_by('nombre'):
            data.append({'id': -1, 'id_lugar': i.id, 'nombre': i.nombre, 'tipo': 'laboratorio',
                         'cantidad_ingreso': 0.0000})
        return data

    @get_model
    def list_desgl_blank(self):
        bodega_model = apps.get_model("bodega", "Bodega")
        laboratorio_model = apps.get_model("tecnicolaboratorio", "Laboratorio")

        data = []
        for i in bodega_model.objects.all().order_by('nombre'):
            data.append({'id': i.id, 'nombre': i.nombre, 'tipo': 'bodega', 'cantidad_ingreso': 0.0000})
        for i in laboratorio_model.objects.all().order_by('nombre'):
            data.append({'id': i.id, 'nombre': i.nombre, 'tipo': 'laboratorio', 'cantidad_ingreso': 0.0000})
        return data

    @get_model
    def permit_delete(self):
        return self._is_del()

    @get_model
    def search_data(self, type_filter, id_s, request):
        data = []
        if type_filter == 'un_med':
            if request.session['group'].name == 'laboratorio':
                query = self.model.objects.filter(unidad_medida_id=id_s,
                                                  stock__laboratorio__responsable_id=request.user.id)
            elif request.session['group'].name == 'bodega':
                query = self.model.objects.filter(unidad_medida_id=id_s, stock__bodega__responsable_id=request.user.id)
            else:
                query = self.model.objects.filter(unidad_medida_id=id_s)
        else:
            if request.session['group'].name == 'laboratorio':
                query = self.model.objects.filter(stock__laboratorio__responsable_id=request.user.id)
            elif request.session['group'].name == 'bodega':
                query = self.model.objects.filter(stock__bodega__responsable_id=request.user.id)
            else:
                query = self.model.objects.all()
        for i in query:
            item = {
                'id': i.id,
                'nombre': i.nombre,
                'cupo_autorizado': i.cupo_autorizado,
                'unidad_medida': i.unidad_medida.nombre
            }
            data.append(item)
        return data

    @get_model
    def search_stock(self, request):
        stock_model = apps.get_model("representantetecnico", "Stock")

        data = []
        if request.session['group'].name == 'laboratorio':
            query = stock_model.objects.filter(laboratorio__responsable_id=request.user.id, sustancia_id=self.object.id)
        elif request.session['group'].name == 'bodega':
            query = stock_model.objects.filter(bodega__responsable_id=request.user.id, sustancia_id=self.object.id)
        else:
            query = stock_model.objects.filter(sustancia_id=self.object.id)
        for i in query:
            item = {'id': i.id, 'cantidad': i.cantidad, 'type': '', 'nombre': ''}
            if i.laboratorio is not None:
                item['type'] = 'laboratorio'
                item['nombre'] = i.laboratorio.nombre
            elif i.bodega is not None:
                item['type'] = 'bodega'
                item['nombre'] = i.bodega.nombre
            data.append(item)
        return data

    @get_model
    def search_sus_bod(self, code_bod, term):
        stock_model = apps.get_model("representantetecnico", "Stock")

        data = []
        for i in stock_model.objects.filter(sustancia__nombre__icontains=term, bodega_id=code_bod)[0:10]:
            item = {'id': i.id, 'cupo_autorizado': i.sustancia.cupo_autorizado, 'value': i.sustancia.nombre,
                    'unidad_medida': i.sustancia.unidad_medida.nombre, 'cantidad_bodega': i.cantidad}
            data.append(item)
        return data

    @staticmethod
    def search_sus_compra(code_bod, term):
        stock_model = apps.get_model("representantetecnico", "Stock")

        data = []
        for stock in stock_model.objects.filter(sustancia__nombre__icontains=term, bodega_id=code_bod)[0:10]:
            item = {'id': stock.id, 'cupo_autorizado': float(stock.sustancia.cupo_autorizado),
                    'value': stock.sustancia.nombre, 'unidad_medida': stock.sustancia.unidad_medida.nombre,
                    'cantidad_bodega': float(stock.cantidad),
                    'cupo_consumido': querysets.get_cupo_consumido(datetime.now().year, stock.sustancia_id)}
            data.append(item)
        return data

    @get_model
    def update_sustancia(self, stock_new):
        with transaction.atomic():
            tipo_mov_inv_model = apps.get_model("representantetecnico", "TipoMovimientoInventario")
            inventario_model = apps.get_model("representantetecnico", "Inventario")

            tipo_movimiento_add = tipo_mov_inv_model.objects.get(nombre='add')
            tipo_movimiento_del = tipo_mov_inv_model.objects.get(nombre='delete')

            self.object.save()

            stock_old = self.object.stock_set.all()

            """Actualizar los stock ya agregados"""
            for st_old in stock_old:
                for st_new in stock_new:
                    if st_old.id == st_new['id']:
                        if float(st_old.cantidad) != st_new['cantidad_ingreso']:
                            inv = inventario_model()
                            inv.stock_id = st_old.id

                            if float(st_old.cantidad) > st_new['cantidad_ingreso']:
                                inv.tipo_movimiento_id = tipo_movimiento_del.id
                                inv.cantidad_movimiento = float(st_old.cantidad) - st_new['cantidad_ingreso']

                            if float(st_old.cantidad) < st_new['cantidad_ingreso']:
                                inv.tipo_movimiento_id = tipo_movimiento_add.id
                                inv.cantidad_movimiento = st_new['cantidad_ingreso'] - float(st_old.cantidad)

                            st_old.cantidad = st_new['cantidad_ingreso']

                            st_old.save()
                            inv.save()
                        break

            """Añadir nuevos stock en caso de que se haya añadido un laboratorio o bodega nuevo"""
            for st_new in stock_new:
                if st_new['id'] == -1:
                    self._add_stock(st_new)
