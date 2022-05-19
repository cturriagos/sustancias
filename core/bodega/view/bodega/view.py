from datetime import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from app.settings import LOGIN_REDIRECT_URL
from core.base import querysets
from core.base.mixins.is_user_ucscsf import IsUserUCSCSF
from core.base.mixins.user_notifications import UserNotifications
from core.base.mixins.validate_permission_required_mixin import ValidatePermissionRequiredMixin
from core.bodega.models import Bodega
from core.representantetecnico.controller.inventario_controller import InventarioController


class BodegaView(LoginRequiredMixin, IsUserUCSCSF, ValidatePermissionRequiredMixin, UserNotifications, TemplateView):
    permission_required = ('bodega.view_bodega',)
    template_name = 'bodega/view.html'
    url_redirect = reverse_lazy('bdg:bodegas')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = Bodega()

    def dispatch(self, request, *args, **kwargs):
        try:
            self.object = Bodega.objects.get(pk=kwargs['pk'])

            return super().dispatch(request, *args, **kwargs)

        except Exception as e:
            messages.error(request, str(e))

        return HttpResponseRedirect(self.url_redirect)

    def get_context_data(self, **kwargs):
        fecha_actual = datetime.now()
        context = super().get_context_data(**kwargs)
        context['url_list'] = self.url_redirect
        context['icontitle'] = 'eye'
        context['title'] = '{} {}'.format("Bodega ", self.object.id)
        context['is_del'] = self.object.controller.permit_delete()
        context['estado_sustancias'] = querysets.get_data_inventario_mov(0, self.object.id,
                                                                         mes=fecha_actual.month,
                                                                         year=fecha_actual.year)
        context['row_names'] = InventarioController.get_colum_names_for_states_months(
            array=context['estado_sustancias'])

        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": self.url_redirect, "uriname": "Bodegas"},
            {"uridj": reverse_lazy('bdg:verbodega', kwargs={'pk': self.object.id}), "uriname": context['title']}
        ]
        return context
