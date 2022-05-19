from core.base.decorators import get_model
from core.base.mixins.controller import Controller


class BodegaController(Controller):
    model_str = "bodega.Bodega"

    @get_model
    def delete_object(self):
        if self.permit_delete() is False:
            raise Exception("No es posible eliminar este registro")
        self.object.delete()

    @get_model
    def permit_delete(self):
        if self.object.compraspublicas_set.all().count() > 0 \
                or self.object.solicitud_set.all().count() > 0 \
                or self.object.stock_set.all().count() > 0:
            return False
        return True

    @get_model
    def search_data(self, request):
        if request.session['group'].name == 'bodega':
            query = self.model.objects.filter(responsable_id=request.user.id)
        else:
            query = self.model.objects.all()
        data = []
        for i in query:
            item = {'id': i.id, 'nombre': i.nombre, 'responsable': i.responsable.controller.get_user_info(),
                    'is_del': i.controller.permit_delete(), 'dir': i.direccion}
            data.append(item)
        return data
