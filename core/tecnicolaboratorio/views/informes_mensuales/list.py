from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins.is_user_ucscsf import IsUserUCSCSF
from core.base.mixins.user_notifications import UserNotifications
from core.base.mixins.validate_permission_required_mixin import ValidatePermissionRequiredMixin
from core.representantetecnico.models import InformesMensuales, Mes


class InformesMensualesListView(LoginRequiredMixin, IsUserUCSCSF, ValidatePermissionRequiredMixin, UserNotifications,
                                ListView):
    permission_required = ('representantetecnico.view_informesmensuales',)
    model = InformesMensuales
    template_name = "informesmensuales/list.html"

    def get(self, request, *args, **kwargs):
        try:
            action = request.GET.get('action')
            result = request.GET.get('result')

            if action == 'searchdata' and result == 'jsondata':

                type_data = request.GET.get('type')
                id_data = request.GET.get('id')

                data = self.model.controller.search_data(type_data, id_data, request)

                return JsonResponse(data, safe=False)

            elif action == 'informe_detail':

                informe_id = request.GET.get('informe_id')

                data = self.model.controller.get_informe_detail(informe_id)

                return JsonResponse(data, safe=False)

        except Exception as e:
            messages.error(request, str(e))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Informes mensuales registrados"
        context['icontitle'] = "store-alt"
        context['meses'] = Mes.objects.all()
        context['years'] = self.model.controller.get_years_in_stock()
        context['create_url'] = reverse_lazy('tl:registroinformesmensuales')
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": reverse_lazy('tl:informesmensuales'), "uriname": "Informes mesuales"}
        ]
        return context
