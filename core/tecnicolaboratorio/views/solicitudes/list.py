from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins.is_user_ucscsf import IsUserUCSCSF
from core.base.mixins.user_notifications import UserNotifications
from core.base.mixins.validate_permission_required_mixin import ValidatePermissionRequiredMixin
from core.representantetecnico.models import Solicitud, EstadoTransaccion
from core.tecnicolaboratorio.models import Laboratorio


class SolicitudListView(LoginRequiredMixin, IsUserUCSCSF, ValidatePermissionRequiredMixin, UserNotifications, ListView):
    permission_required = ('representantetecnico.view_solicitud',)
    model = Solicitud
    template_name = "solicitud/list.html"

    def get(self, request, *args, **kwargs):
        try:
            action = request.GET.get('action')
            result = request.GET.get('result')

            if action == 'search_sol_rec':
                id_stock = int(request.GET.get('stock_id'))
                det_inf = int(request.GET.get('det_inf'))

                data = self.model.controller.search_sol_rec(id_stock, det_inf, request)

                return JsonResponse(data, safe=False)

            elif action == 'searchdata' and result == 'jsondata':
                type_data = request.GET.get('type')
                id_data = request.GET.get('id')

                data = self.model.controller.search_data(type_data, id_data, request)

                return JsonResponse(data, safe=False)

            elif action == 'search_detalle':
                id_sl = request.GET.get('id_sl')
                data = self.model.controller.search_detalle_sin_sesion(id_sl)

                return JsonResponse(data, safe=False)

        except Exception as e:
            messages.error(request, str(e))

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Solicitudes registradas"
        context['icontitle'] = "store-alt"
        context['estados'] = EstadoTransaccion.objects.all()
        context['create_url'] = reverse_lazy('tl:registrosolicitud')
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": reverse_lazy('tl:solicitudes'), "uriname": "Solicitudes"}
        ]

        if self.request.session['group'].name != 'laboratorio':
            context['laboratorios'] = Laboratorio.objects.all()

        return context
