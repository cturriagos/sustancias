import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins.is_user_ucscsf import IsUserUCSCSF
from core.base.mixins.user_notifications import UserNotifications
from core.base.mixins.validate_permission_required_mixin import ValidatePermissionRequiredMixin
from core.bodega.forms.sustancia_form import SustanciaForm
from core.representantetecnico.models import Sustancia


class SustanciaCreateView(LoginRequiredMixin, IsUserUCSCSF, ValidatePermissionRequiredMixin, UserNotifications,
                          CreateView):
    permission_required = ('representantetecnico.add_sustancia',)
    model = Sustancia
    form_class = SustanciaForm
    template_name = "sustancia/create.html"
    success_url = reverse_lazy("bdg:sustancias")
    url_redirect = success_url

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':

                form = self.get_form()

                if form.is_valid():
                    self.object = form.instance

                    lugares = json.loads(request.POST['desgloses'])

                    self.object.controller.crear_sustancia(lugares)

                    data['url'] = reverse_lazy('bdg:versustancias', kwargs={'pk': self.object.id})

                else:
                    data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Registro de sustancias"
        context['icontitle'] = "plus"
        context['url_list'] = self.success_url
        context['action'] = 'add'
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": self.success_url, "uriname": "Sustancias"},
            {"uridj": reverse_lazy('bdg:registrosustancias'), "uriname": "Registro"}
        ]
        return context
