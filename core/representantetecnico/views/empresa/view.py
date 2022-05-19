from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins.is_user_ucscsf import IsUserUCSCSF
from core.base.mixins.user_notifications import UserNotifications
from core.base.mixins.validate_permission_required_mixin import ValidatePermissionRequiredMixin
from core.representantetecnico.models import Proveedor


class EmpresaView(LoginRequiredMixin, IsUserUCSCSF, ValidatePermissionRequiredMixin, UserNotifications, TemplateView):
    permission_required = ('representantetecnico.view_proveedor',)
    template_name = 'empresa/view.html'
    url_redirect = reverse_lazy('rp:empresas')

    def dispatch(self, request, *args, **kwargs):
        try:

            self.object = Proveedor.objects.get(pk=kwargs['pk'])

            return super().dispatch(request, *args, **kwargs)

        except Exception as e:
            messages.error(request, str(e))

        return HttpResponseRedirect(self.url_redirect)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_list'] = self.url_redirect
        context['icontitle'] = 'eye'
        context['title'] = '{} {}'.format("Proveedor ", self.object.id)
        context['is_del'] = self.object.controller.permit_delete()
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": self.url_redirect, "uriname": "Proveedores"},
            {"uridj": reverse_lazy('rp:vercompras', kwargs={'pk': self.object.id}), "uriname": context['title']}
        ]
        return context
