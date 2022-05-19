from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins.is_user_ucscsf import IsUserUCSCSF
from core.base.mixins.user_notifications import UserNotifications
from core.base.mixins.validate_permission_required_mixin import ValidatePermissionRequiredMixin
from core.representantetecnico.models import InformesMensuales
from core.tecnicolaboratorio.forms.desglose_sustancia_informe_mensual_form import DesgloseSustanciaInformeMensualForm
from core.tecnicolaboratorio.forms.informe_mensual_form import InformeMensualForm
from core.tecnicolaboratorio.models import Proyecto


class InformesMensualesUpdateView(LoginRequiredMixin, IsUserUCSCSF, ValidatePermissionRequiredMixin,
                                  UserNotifications, UpdateView):
    permission_required = ('representantetecnico.change_informesmensuales',)
    model = InformesMensuales
    form_class = InformeMensualForm
    template_name = "informesmensuales/create.html"
    success_url = reverse_lazy("tl:informesmensuales")
    url_redirect = success_url
    action = 'edit'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def get(self, request, *args, **kwargs):
        try:
            action = request.GET.get('action')

            if action == 'informe_detail':
                data = self.object.controller.get_informe_detail()

                return JsonResponse(data, safe=False)

        except Exception as e:
            messages.error(request, str(e))

        return super().get(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            self.object.controller.validate_access(request)
        except Exception as e:
            messages.error(request, str(e))
            return HttpResponseRedirect(self.success_url)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        current_lab_user = self.request.user.laboratorio_set.first()
        context = super().get_context_data(**kwargs)
        context['title'] = "Actualizar informe mensual"
        context['icontitle'] = "edit"
        context['url_list'] = self.success_url
        context['form_desglose'] = DesgloseSustanciaInformeMensualForm(initial={
            'proyecto': Proyecto.objects.filter(laboratorio_id=current_lab_user.id)
        })
        context['action'] = self.action
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": self.success_url, "uriname": "Informes mensuales"},
            {"uridj": reverse_lazy('tl:actualizacioninformesmensuales', kwargs={'pk': self.object.id}),
             "uriname": "Edicción"}
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

                    self.object.controller.update_object(request)

                    data['url'] = reverse_lazy('tl:verinformesmensuales', kwargs={'pk': self.object.id})

                else:
                    data['error'] = form.errors

        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data, safe=False)
