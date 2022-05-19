import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins.is_user_ucscsf import IsUserUCSCSF
from core.base.mixins.user_notifications import UserNotifications
from core.base.mixins.validate_permission_required_mixin import ValidatePermissionRequiredMixin
from core.bodega.forms.sustancia_form import SustanciaForm
from core.representantetecnico.models import Sustancia


class SustanciaUpdateView(LoginRequiredMixin, IsUserUCSCSF, ValidatePermissionRequiredMixin, UserNotifications,
                          UpdateView):
    permission_required = ('representantetecnico.change_sustancia',)
    model = Sustancia
    form_class = SustanciaForm
    template_name = 'sustancia/create.html'
    success_url = reverse_lazy('bdg:sustancias')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):

        self.object = self.get_object()

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Actualizar sustancia"
        context['icontitle'] = "edit"
        context['url_list'] = self.success_url
        context['action'] = 'edit'
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": self.success_url, "uriname": "Sustancia"},
            {"uridj": reverse_lazy('bdg:actualizacionsustancia', kwargs={'pk': self.object.id}), "uriname": "Edicción"}
        ]
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')

            if action == 'edit':
                form = self.get_form()

                if form.is_valid():

                    self.object = form.instance

                    stock_new = json.loads(request.POST['desgloses'])

                    self.object.controller.update_sustancia(stock_new)

                    data['url'] = reverse_lazy('bdg:versustancias', kwargs={'pk': self.object.controller.object.id})

                else:
                    data['error'] = form.errors

        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data, safe=False)
