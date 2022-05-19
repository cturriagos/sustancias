from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins.is_user_ucscsf import IsUserUCSCSF
from core.base.mixins.user_notifications import UserNotifications
from core.base.mixins.validate_permission_required_mixin import ValidatePermissionRequiredMixin
from core.tecnicolaboratorio.models import Proyecto


class ProyectoDeleteView(LoginRequiredMixin, IsUserUCSCSF, ValidatePermissionRequiredMixin, UserNotifications,
                         DeleteView):
    permission_required = ('tecnicolaboratorio.delete_proyecto',)
    model = Proyecto
    template_name = 'delete.html'
    success_url = reverse_lazy('tl:proyectos')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.controller.permit_delete() is False:
            messages.error(request, 'No es posible eliminar este registro')
            messages.error(request, 'Pongase en contacto con el administrador del sistema')
            return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}

        try:
            self.object.controller.delete_object()

        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Eliminar proyecto"
        context['icontitle'] = "trash-alt"
        context['url_list'] = self.success_url
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": self.success_url, "uriname": "Proyectos"},
            {"uridj": reverse_lazy('tl:eliminarproyecto', kwargs={'pk': self.object.id}), "uriname": "Eliminar"}
        ]
        return context
