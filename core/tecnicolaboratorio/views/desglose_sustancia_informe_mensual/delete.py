from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from core.base.mixins.is_user_ucscsf import IsUserUCSCSF
from core.base.mixins.validate_permission_required_mixin import ValidatePermissionRequiredMixin
from core.representantetecnico.models import DesgloseInfomeMensualDetalle


class DesgloseSustanciaInformeMensualDeleteView(LoginRequiredMixin, IsUserUCSCSF, ValidatePermissionRequiredMixin,
                                                DeleteView):
    permission_required = ('representantetecnico.delete_desgloseinfomemensualdetalle',)
    model = DesgloseInfomeMensualDetalle
    template_name = 'desglosesustanciainformemensual/delete.html'
    success_url = reverse_lazy('tl:informesmensuales')
    url_redirect = success_url

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.controller.permit_delete() is False:
            messages.error(request, 'Informe actual ya esta cerrado')
            messages.error(request, 'No es posible realizar operaciones sobre el mismo')
            messages.error(request, 'Pongase en contacto con el administrador del sistema')
            return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.controller.delete_object()
        except Exception as e:
            messages.error(request, str(e))
        return JsonResponse(data)
