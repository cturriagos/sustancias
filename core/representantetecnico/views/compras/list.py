from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins.is_user_ucscsf import IsUserUCSCSF
from core.base.mixins.user_notifications import UserNotifications
from core.base.mixins.validate_permission_required_mixin import ValidatePermissionRequiredMixin
from core.representantetecnico.models import ComprasPublicas, EstadoTransaccion, Proveedor


class ComprasListView(LoginRequiredMixin, IsUserUCSCSF, ValidatePermissionRequiredMixin, UserNotifications, ListView):
    permission_required = ('representantetecnico.view_compraspublicas',)
    model = ComprasPublicas
    template_name = "compras/list.html"

    def get(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.GET.get('action')
            result = request.GET.get('result')

            if action == 'searchdata' and result == 'jsondata':
                id_s = request.GET.get('id')
                type_filter = request.GET.get('type')

                data = self.model.controller.search_data(type_filter, id_s, request)

                return JsonResponse(data, safe=False)

        except Exception as e:
            data['error'] = str(e)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Compras registradas"
        context['icontitle'] = "store-alt"
        context['estados'] = EstadoTransaccion.objects.all()
        context['convocatorias'] = self.model.controller.get_convocatorias_compra()
        context['empresas'] = Proveedor.objects.all()
        context['create_url'] = reverse_lazy('rp:registrocompras')
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": reverse_lazy('rp:compras'), "uriname": "Compras"}
        ]
        return context
