from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins.is_user_ucscsf import IsUserUCSCSF
from core.base.mixins.user_notifications import UserNotifications
from core.base.mixins.validate_permission_required_mixin import ValidatePermissionRequiredMixin
from core.tecnicolaboratorio.models import Laboratorio


class LaboratorioListView(LoginRequiredMixin, IsUserUCSCSF, ValidatePermissionRequiredMixin, UserNotifications,
                          ListView):
    permission_required = ('tecnicolaboratorio.view_laboratorio',)
    model = Laboratorio
    template_name = "laboratorio/list.html"

    def get(self, request, *args, **kwargs):
        try:
            action = request.GET.get('action')
            result = request.GET.get('result')

            if action == 'searchdata' and result == 'jsondata':

                data = self.model.controller.search_data(request)

                return JsonResponse(data, safe=False)

            elif action == 'search_sus_lab':

                current_lab_user = request.user.laboratorio_set.first()
                term = request.GET.get('term')

                data = current_lab_user.controller.search_sus_lab(term)

                return JsonResponse(data, safe=False)

            elif action == 'search_months_dsp':

                current_lab_user = request.user.laboratorio_set.first()

                year = request.GET.get('year')

                data = current_lab_user.controller.search_months_dsp(year)

                return JsonResponse(data, safe=False)

        except Exception as e:
            messages.error(request, str(e))

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Laboratorios registrados"
        context['icontitle'] = "store-alt"
        context['create_url'] = reverse_lazy('tl:registrolaboratorio')
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": reverse_lazy('tl:laboratorios'), "uriname": "Laboratorios"}
        ]
        return context
