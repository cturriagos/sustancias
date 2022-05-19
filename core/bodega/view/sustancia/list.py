from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView

from app.settings import LOGIN_REDIRECT_URL
from core.base import querysets
from core.base.mixins.is_user_ucscsf import IsUserUCSCSF
from core.base.mixins.user_notifications import UserNotifications
from core.base.mixins.validate_permission_required_mixin import ValidatePermissionRequiredMixin
from core.representantetecnico.models import Sustancia, UnidadMedida


class SustanciaListView(LoginRequiredMixin, IsUserUCSCSF, ValidatePermissionRequiredMixin, UserNotifications, ListView):
    permission_required = ('representantetecnico.view_sustancia',)
    model = Sustancia
    template_name = "sustancia/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Sustancias registradas"
        context['icontitle'] = "store-alt"
        context['unidades'] = UnidadMedida.objects.all()
        context['create_url'] = reverse_lazy('bdg:registrosustancias')
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": reverse_lazy('bdg:sustancias'), "uriname": "Sustancias"}
        ]
        return context

    def get(self, request, *args, **kwargs):
        try:
            action = request.GET.get('action')
            result = request.GET.get('result')

            if action == 'searchdata' and result == 'jsondata':
                id_s = request.GET.get('id')
                type_filter = request.GET.get('type')

                data = self.model.controller.search_data(type_filter, id_s, request)

                return JsonResponse(data, safe=False)

            elif action == 'search_sus_compra':
                code_bod = request.GET.get('code_bod')
                term = request.GET.get('term')

                data = self.model.controller.search_sus_compra(code_bod, term)

                return JsonResponse(data, safe=False)

            elif action == 'search_sus_bod':
                code_bod = request.GET.get('code_bod')
                term = request.GET.get('term')

                data = self.model.controller.search_sus_bod(code_bod, term)

                return JsonResponse(data, safe=False)

            elif action == 'search_sus_bod_lab':
                code_bod = request.GET.get('code_bod')
                term = request.GET.get('term')
                code_lab = request.user.laboratorio_set.first()

                data = querysets.get_substances_solicitud(code_lab.id, code_bod, term)

                return JsonResponse(data, safe=False)

            elif action == 'list_desgl_blank':
                data = self.model.controller.list_desgl_blank()

                return JsonResponse(data, safe=False)

        except Exception as e:
            messages.error(request, str(e))

        return super().get(request, *args, **kwargs)
