from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins.is_user_ucscsf import IsUserUCSCSF
from core.base.mixins.user_notifications import UserNotifications
from core.base.mixins.validate_permission_required_mixin import ValidatePermissionRequiredMixin
from core.base.querysets import get_years_disp_inv
from core.representantetecnico.models import Inventario, Mes, Sustancia


class MovimientosInventarioListView(LoginRequiredMixin, IsUserUCSCSF, ValidatePermissionRequiredMixin,
                                    UserNotifications, ListView):
    permission_required = ('representantetecnico.view_inventario',)
    model = Inventario
    template_name = "movimientosinventario/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Movimientos inventario"
        context['icontitle'] = "store-alt"
        context['years_disp'] = get_years_disp_inv()
        context['sustancias'] = Sustancia.objects.all()
        context['meses'] = Mes.objects.all()
        context['create_url'] = reverse_lazy('rp:registrocompras')
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": reverse_lazy('bdg:sustancias'), "uriname": "Inventario"},
            {"uridj": reverse_lazy('rp:movimientoinventario'), "uriname": "Movimientos"}
        ]
        return context

    def get(self, request, *args, **kwargs):
        try:
            action = request.GET.get('action')
            result = request.GET.get('result')

            if action == 'searchdata' and result == 'jsondata':
                _id = request.GET.get('id')
                _year = request.GET.get('year')
                _type = request.GET.get('type')

                data = self.model.controller.search_data_mov(request, _type, _year, _id)

                return JsonResponse(data, safe=False)

        except Exception as e:
            messages.error(request, str(e))

        return super().get(request, *args, **kwargs)
