import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins.is_user_ucscsf import IsUserUCSCSF
from core.base.mixins.user_notifications import UserNotifications
from core.base.mixins.validate_permission_required_mixin import ValidatePermissionRequiredMixin
from core.representantetecnico.forms.compra_form import ComprasForm
from core.representantetecnico.models import ComprasPublicas


class ComprasUpdateView(LoginRequiredMixin, IsUserUCSCSF, ValidatePermissionRequiredMixin, UserNotifications,
                        UpdateView):
    permission_required = ('representantetecnico.change_compraspublicas',)
    model = ComprasPublicas
    form_class = ComprasForm
    template_name = 'compras/create.html'
    success_url = reverse_lazy('rp:compras')
    url_redirect = success_url

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.controller.permit_delete() is False:
            messages.error(request, 'Registro de compra ya almacenado en bodega')
            messages.error(request, 'No es posible su modificación')
            messages.error(request, 'Pongase en contacto con el administrador del sistema')
            return HttpResponseRedirect(self.success_url)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Actualizar compra"
        context['icontitle'] = "edit"
        context['url_list'] = self.success_url
        context['action'] = 'edit'
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": self.success_url, "uriname": "Compras"},
            {"uridj": reverse_lazy('rp:registrocompras'), "uriname": "Edicción"}
        ]
        return context

    def get(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.GET.get('action')
            if action is not None:

                if action == 'searchdetail':
                    data = self.object.controller.search_detail()

                    return JsonResponse(data, safe=False)

        except Exception as e:
            data['error'] = str(e)

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')
            if action == 'edit':

                form = self.get_form()

                if form.is_valid():

                    self.object = form.instance

                    detalle_compras_new = json.loads(request.POST['detalle_compra'])

                    self.object.controller.actualizar_compra(detalle_compras_new)

                    data['url'] = reverse_lazy('rp:vercompras', kwargs={'pk': self.object.id})

                else:
                    data['error'] = form.errors

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
