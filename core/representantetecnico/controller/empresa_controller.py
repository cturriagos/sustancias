from core.base.decorators import get_model
from core.base.mixins.controller import Controller


class EmpresaController(Controller):
    model_str = "representantetecnico.Proveedor"

    @get_model
    def delete_object(self):
        if self.permit_delete() is False:
            raise Exception('No es posible eliminar este registro')
        self.object.delete()

    @get_model
    def permit_delete(self):
        if self.object.compraspublicas_set.all().count() > 0:
            return False
        return True

    @get_model
    def search_data(self):
        data = []
        for bdg in self.model.objects.all():
            item = {'id': bdg.id, 'nombre': bdg.nombre, 'ruc': bdg.ruc}
            data.append(item)
        return data
