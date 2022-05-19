from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View

from core.base.mixins.is_user_ucscsf import IsUserUCSCSF
from core.base.mixins.validate_permission_required_mixin import ValidatePermissionRequiredMixin
from core.representantetecnico.models import DesgloseInfomeMensualDetalle


class DesgloseSustanciaInformeMensualListView(LoginRequiredMixin, IsUserUCSCSF, ValidatePermissionRequiredMixin, View):
    permission_required = ('representantetecnico.view_desgloseinfomemensualdetalle',)
    url_redirect = reverse_lazy('tl:informesmensuales')

    def get(self, request, *args, **kwargs):
        try:
            action = request.GET.get('action')

            if action == 'search_desglose_sustancia':
                detalle_informe_id = int(request.GET.get('detalle_informe_id'))

                data = DesgloseInfomeMensualDetalle.controller.search_desglose_sustancia(detalle_informe_id)

                return JsonResponse(data, safe=False)

        except Exception as e:
            messages.error(request, str(e))

        return HttpResponseRedirect(self.url_redirect)
