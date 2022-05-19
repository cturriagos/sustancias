from datetime import datetime

from django.apps import apps

from core.base.decorators import get_model
from core.base.mixins.controller import Controller


class LaboratorioController(Controller):
    model_str = "tecnicolaboratorio.Laboratorio"

    def get_choices_months_disp_year(self, year=None):
        choices = []
        choices += [(o['id'], o['text']) for o in self.search_months_dsp(year)]
        return choices

    def delete_object(self):
        if self.permit_delete() is False:
            raise Exception('No es posible eliminar este registro')

        self.object.delete()

    def permit_delete(self):
        if self.object.stock_set.all().count() > 0:
            return False

        return True

    @get_model
    def search_data(self, request):
        data = []
        if request.session['group'].name == 'laboratorio':
            query = self.model.objects.filter(responsable_id=request.user.id)
        else:
            query = self.model.objects.all()

        for i in query:
            item = {'id': i.id, 'nombre': i.nombre, 'responsable': '', 'dir': i.direccion}

            if i.responsable is not None:
                item['responsable'] = i.responsable.controller.get_user_info()

            data.append(item)

        return data

    def search_months_dsp(self, year=None):
        if year is None:
            year = datetime.now().year

        mes_model = apps.get_model("representantetecnico", "Mes")

        data = []

        query = mes_model.objects.exclude(informesmensuales__year=year,
                                          informesmensuales__laboratorio_id=self.object.id)

        for y in query:
            data.append({'id': y.id, 'text': y.nombre})

        return data

    def search_sus_lab(self, term):
        stock_model = apps.get_model("representantetecnico", "Stock")

        data = []
        for stock in stock_model.objects.filter(sustancia__nombre__icontains=term, laboratorio_id=self.object.id)[0:10]:
            if stock.cantidad > 0:
                data.append({
                    'id': stock.id,
                    'value': stock.sustancia.nombre,
                    'unidad_medida': stock.sustancia.unidad_medida.nombre,
                    'cantidad_lab': stock.cantidad
                })
        return data
