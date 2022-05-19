from django.apps import apps
from django.db import transaction
from django.db.models import Sum
from django.db.models.functions import Coalesce

from app.settings import MEDIA_URL
from core.base.decorators import get_model
from core.base.mixins.controller import Controller


class DesgloseInfomeMensualDetalleController(Controller):
    model_str = "representantetecnico.DesgloseInfomeMensualDetalle"

    @get_model
    def create_object(self, id_detalle):
        with transaction.atomic():
            informe_detalle_model = apps.get_model("representantetecnico", "InformesMensualesDetalle")

            if self.object.cantidad <= 0:
                raise Exception('Debe ingresar una cantidad de consumo valida')

            suma_desgloses = self.model.objects.filter(informe_mensual_detalle_id=id_detalle).aggregate(
                total=Coalesce(Sum('cantidad'), 0))

            total_desgloses = float(suma_desgloses['total']) + float(self.object.cantidad)

            informe_detalle = informe_detalle_model.objects.get(pk=id_detalle)

            if float(informe_detalle.cantidad) < total_desgloses:
                raise Exception('La cantidad total del desglose no puede exceder el consumo de sustancia declarado')

            self.object.informe_mensual_detalle_id = id_detalle
            self.object.save()

    @get_model
    def delete_object(self):
        if self.permit_delete() is False:
            raise Exception('No es posible eliminar este registro')

        self.object.delete()

    @get_model
    def get_documento(self):
        if self.object.documento:
            return '{}{}'.format(MEDIA_URL, self.object.documento)
        return ''

    @get_model
    def permit_delete(self):
        if self.object.informe_mensual_detalle.informe.estado_informe.estado == "archivado":
            return False

        return True

    @get_model
    def search_desglose_sustancia(self, detalle_informe_id):
        data = []

        for desglose in self.model.objects.filter(informe_mensual_detalle_id=detalle_informe_id):

            item = {
                'id': desglose.id,
                'proyecto': "No asignado",
                'responsable': '',
                'cantidad': desglose.cantidad,
                'documento': desglose.controller.get_documento()
            }

            if desglose.proyecto is not None:
                item['proyecto'] = desglose.proyecto.nombre
                item['responsable'] = desglose.proyecto.responsable.__str__()

            data.append(item)

        return data
