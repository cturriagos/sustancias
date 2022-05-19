from datetime import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from app.settings import LOGIN_REDIRECT_URL
from core.base import querysets
from core.base.mixins.is_user_ucscsf import IsUserUCSCSF
from core.base.mixins.user_notifications import UserNotifications
from core.base.mixins.validate_permission_required_mixin import ValidatePermissionRequiredMixin
from core.representantetecnico.controller.inventario_controller import InventarioController
from core.representantetecnico.forms.estado_mensual_form import EstadoMensualFiltrosForm
from core.representantetecnico.models import Mes


class EstadoMensualListView(LoginRequiredMixin, IsUserUCSCSF, ValidatePermissionRequiredMixin, UserNotifications,
                            TemplateView):
    permission_required = ('representantetecnico.view_inventario',)
    template_name = "movimientosinventario/estadomensual.html"
    url_redirect = reverse_lazy('rp:movimientoinventario')

    def __init__(self, *args, **kwargs):
        self.controller = InventarioController()
        super().__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        years = querysets.get_years_disp_inv()
        fecha_actual = datetime.now()
        estado_sustancias = self.controller.search_data_est(request=self.request, mes=fecha_actual.month,
                                                            year=fecha_actual.year)

        context = super().get_context_data(**kwargs)
        context['title'] = "Estado mensual de sustancias"
        context['icontitle'] = "store-alt"
        context['year'] = fecha_actual.year
        context['year_min'] = context['year']
        context['year_max'] = context['year']
        context['estado_mensual_form'] = EstadoMensualFiltrosForm(
            initial={'mes': Mes.objects.get(numero=fecha_actual.month)})
        context['row_names'] = self.controller.get_colum_names_for_states_months(array=estado_sustancias)
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": reverse_lazy('bdg:sustancias'), "uriname": "Inventario"},
            {"uridj": reverse_lazy('rp:estadomensual'), "uriname": "Estados mensuales"}
        ]

        if len(years) > 0:
            year_min = min(years, key=lambda k: k['anio'])
            year_max = max(years, key=lambda k: k['anio'])
            context['year_min'] = year_min['anio']
            context['year_max'] = year_max['anio']

        return context

    def get(self, request, *args, **kwargs):
        try:
            action = request.GET.get('action')
            if action == 'searchdata':
                mes = request.GET.get('mes')
                year = request.GET.get('year')

                data = self.controller.search_data_est(request, mes, year)

                return JsonResponse(data, safe=False)

        except Exception as e:
            messages.error(request, str(e))

        return super().get(request, *args, **kwargs)
