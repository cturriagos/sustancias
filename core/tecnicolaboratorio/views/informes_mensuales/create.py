from datetime import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins.is_user_ucscsf import IsUserUCSCSF
from core.base.mixins.user_notifications import UserNotifications
from core.base.mixins.validate_permission_required_mixin import ValidatePermissionRequiredMixin
from core.representantetecnico.models import InformesMensuales, Mes
from core.tecnicolaboratorio.forms.informe_mensual_form import InformeMensualForm


class InformesMensualesCreateView(LoginRequiredMixin, IsUserUCSCSF, ValidatePermissionRequiredMixin,
                                  UserNotifications, CreateView):
    permission_required = ('representantetecnico.add_informesmensuales',)
    model = InformesMensuales
    form_class = InformeMensualForm
    template_name = "informesmensuales/create.html"
    success_url = reverse_lazy("tl:informesmensuales")
    url_redirect = success_url
    action = 'add'

    def dispatch(self, request, *args, **kwargs):
        if self.model.controller.validate_creation(current_user=request.user) is False:
            messages.error(request, 'Aun existen informes por archivar')
            messages.error(request, 'Debe archivar todos los informes antes de crear otro')

            return HttpResponseRedirect(self.success_url)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Registro informes mensuales de laboratorio"
        context['icontitle'] = "plus"
        context['url_list'] = self.success_url
        context['action'] = self.action
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": self.success_url, "uriname": "Solicitudes"},
            {"uridj": reverse_lazy('tl:registroinformesmensuales'), "uriname": "Registro"}
        ]
        return context

    def get_form_kwargs(self):
        current_lab_user = self.request.user.laboratorio_set.first()
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'mes': Mes.objects.exclude(informesmensuales__year=datetime.now().year,
                                                        informesmensuales__laboratorio_id=current_lab_user.id)}
        return kwargs

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')
            if action == 'add':
                form = self.get_form()

                if form.is_valid():

                    self.object = form.instance

                    self.object.controller.create_object(request)

                    data['url'] = reverse_lazy('tl:actualizacioninformesmensuales',
                                               kwargs={'pk': self.object.id})

                else:
                    data['error'] = form.error
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data)
