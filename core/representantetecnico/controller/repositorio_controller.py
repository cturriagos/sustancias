from django.apps import apps
from django.db import transaction
from django.urls import reverse_lazy

from core.base.decorators import get_model
from core.base.formaters import format_datetime
from core.base.mixins.controller import Controller


class RepositorioController(Controller):
    model_str = "representantetecnico.Repositorio"
    repositorios_validos = ['personal', 'general', 'externo']

    def activate_all_child_recile_bin(self):
        self.object.is_recicle_bin = True
        self.object.save()

        for rep in self.object.repositorio_set.all():
            rep.controller.activate_all_child_recile_bin()

    @get_model
    def delete_item(self, request):
        id_item = request.POST.get('id')

        if id_item is None:
            raise Exception('Faltan datos')

        with transaction.atomic():

            self._object = self.model.objects.get(pk=id_item)

            if self._object.tipo_repositorio.nombre in ['general', 'externo']:
                if request.user.id != self._object.user_creation.id:
                    if request.session['group'].name != 'representante':
                        raise Exception("Accion no permitida, permisos para manipular este archivo son insuficientes")

            if self._object.is_recicle_bin:
                self._object.delete()
            else:
                self._object.controller.activate_all_child_recile_bin()

    def _get_content_model_repositorio(self, queryset):
        data = []
        for content in queryset.order_by('is_file', 'is_dir'):

            item = {'id': content.id, 'nombre': content.nombre,
                    'create_date': format_datetime(content.date_creation),
                    'url': '', 'is_file': content.is_file, 'is_dir': content.is_dir,
                    'is_recicler': content.is_recicle_bin, 'parent': 0}

            if content.is_file:
                item['url'] = content.documento.url

            if self.object is not None and self.object.id is not None:
                item['parent'] = self.object.id

            data.append(item)

        return data

    def _get_content_model_compras(self):
        model_compras = apps.get_model('representantetecnico', 'ComprasPublicas')
        queryset = model_compras.objects.all()
        data = []
        for content in queryset:
            item = {'id': content.id, 'nombre': "Compra {}".format(content.id),
                    'create_date': format_datetime(content.date_creation),
                    'url': '', 'is_file': False, 'is_dir': True, 'parent': 0}

            data.append(item)

        return data

    def _get_content_model_compras_single(self, pk):
        model_compras = apps.get_model('representantetecnico', 'ComprasPublicas')
        queryset = model_compras.objects.get(pk=pk)
        data = []
        item = {'id': queryset.id, 'nombre': "Documento compra {}".format(queryset.id),
                'create_date': format_datetime(queryset.date_creation),
                'url': '', 'is_file': True, 'is_dir': False, 'parent': queryset.id}

        data.append(item)

        return data

    @get_model
    def get_content(self, request):
        type_content = request.GET.get('type')
        code = request.GET.get('code')

        if int(code) > 0:
            if type_content == 'repository':
                query = self.model.objects.filter(user_creation_id=request.user.id, parent_id=self.object.id,
                                                  is_recicle_bin=False, tipo_repositorio__nombre="personal")
                return self._get_content_model_repositorio(query)
            elif type_content == 'recicle':
                query = self.model.objects.filter(user_creation_id=request.user.id, parent_id=self.object.id,
                                                  is_recicle_bin=True)
                return self._get_content_model_repositorio(query)
            # elif type_content == 'compras':
            #
            #     return []
        else:
            if type_content == 'repository':
                query = self.model.objects.filter(user_creation_id=request.user.id, parent=None, is_recicle_bin=False,
                                                  tipo_repositorio__nombre="personal")
                return self._get_content_model_repositorio(query)
            elif type_content == 'archgen':
                query = self.model.objects.filter(is_recicle_bin=False, tipo_repositorio__nombre="general")
                return self._get_content_model_repositorio(query)
            elif type_content == 'archext':
                query = self.model.objects.filter(is_recicle_bin=False, tipo_repositorio__nombre="externo")
                return self._get_content_model_repositorio(query)
            elif type_content == 'recicle':
                query = self.model.objects.filter(user_creation_id=request.user.id, parent=None, is_recicle_bin=True)
                return self._get_content_model_repositorio(query)
            # elif type_content == 'compras':
            #     return self._get_content_model_compras()

        return []

    @get_model
    def get_path_uris(self):

        items = []
        repositorio = self._object

        while repositorio is not None and repositorio.id is not None:
            items.append({'id': repositorio.id, 'nombre': repositorio.nombre})
            repositorio = repositorio.parent

        return items

    def restore_all_child_recile_bin(self):
        self.object.is_recicle_bin = False
        self.object.save()

        for rep in self.object.repositorio_set.all():
            rep.controller.restore_all_child_recile_bin()

    @get_model
    def restore_item(self, id_item):
        if id_item is not None:

            with transaction.atomic():
                self.object = self.model.objects.get(pk=id_item)
                self.restore_all_child_recile_bin()

        else:
            raise Exception('Faltan datos')

    def search_content(self, request):
        return {'data': self.get_content(request),
                'urlrepository': reverse_lazy('rp:repositorio'),
                'ruta': self.get_path_uris()}
