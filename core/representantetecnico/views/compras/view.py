from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins.is_user_ucscsf import IsUserUCSCSF
from core.base.mixins.user_notifications import UserNotifications
from core.base.mixins.validate_permission_required_mixin import ValidatePermissionRequiredMixin
from core.representantetecnico.models import ComprasPublicas


class ComprasView(LoginRequiredMixin, IsUserUCSCSF, ValidatePermissionRequiredMixin, UserNotifications, TemplateView):
    permission_required = ('representantetecnico.view_compraspublicas',)
    template_name = 'compras/view.html'
    url_redirect = reverse_lazy('rp:compras')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def dispatch(self, request, *args, **kwargs):
        try:
            self.object = ComprasPublicas.objects.get(pk=kwargs['pk'])

            return super().dispatch(request, *args, **kwargs)

        except Exception as e:
            messages.error(request, str(e))

        return HttpResponseRedirect(self.url_redirect)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_list'] = self.url_redirect
        context['icontitle'] = 'eye'
        context['title'] = '{} {}'.format("Compra", self.object.id)
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": self.url_redirect, "uriname": "Compras"},
            {"uridj": reverse_lazy('rp:vercompras', kwargs={'pk': self.object.id}), "uriname": context['title']}
        ]
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'revisionCompra':
                observacion = request.POST.get('observacion')

                if self.object.bodega.responsable_id != request.user.id:
                    raise Exception(
                        "No puede realizar acciones sobre esta compra, no tiene esta bodega asignada")

                self.object.controller.revision_compra(observacion)

            elif action == 'confirmarCompra':

                observacion = request.POST.get('observacion')

                if self.object.bodega.responsable_id != request.user.id:
                    raise Exception(
                        "No puede realizar acciones sobre esta compra, no tiene esta bodega asignada")

                self.object.controller.confirmar_compra(observacion)

            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)
