from core.base.decorators import get_model
from core.base.formaters import format_datetime
from core.base.mixins.controller import Controller


class ProyectoController(Controller):
    model_str = "tecnicolaboratorio.Proyecto"

    def create_object(self, request):
        if request.session['group'].name == 'laboratorio':
            lab_current_user = request.user.laboratorio_set.first()
            self.object.laboratorio_id = lab_current_user.id

        self.object.save()

    def delete_object(self):
        if self.permit_delete() is False:
            raise Exception("No es posible eliminar este registro")
        self.object.delete()

    @get_model
    def permit_delete(self):
        pass

    @get_model
    def search_data(self, request):
        data = []

        if request.session['group'].name == 'laboratorio':
            current_laboratory_user = request.user.laboratorio_set.first()
            query = self.model.objects.filter(laboratorio_id=current_laboratory_user.id)
        else:
            query = self.model.objects.all()

        for i in query:
            item = {'id': i.id, 'nombre': i.nombre, 'lab': "", 'resp': "",
                    'fecha_in': format_datetime(i.fecha_inicio, is_time=False),
                    'fecha_fn': format_datetime(i.fecha_fin, is_time=False)}

            if request.session['group'].name != 'laboratorio':
                item['lab'] = i.laboratorio.nombre

            if i.responsable is not None:
                item['resp'] = i.responsable.get_full_name()

            data.append(item)

        return data

    def update_object(self, request):
        self.create_object(request)
