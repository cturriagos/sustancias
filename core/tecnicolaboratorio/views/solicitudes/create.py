from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins.is_user_ucscsf import IsUserUCSCSF
from core.base.mixins.user_notifications import UserNotifications
from core.base.mixins.validate_permission_required_mixin import ValidatePermissionRequiredMixin
from core.representantetecnico.models import Solicitud
from core.tecnicolaboratorio.forms.solicitud_form import SolicitudForm
from core.tecnicolaboratorio.models import Proyecto


class SolicitudCreateView(LoginRequiredMixin, IsUserUCSCSF, ValidatePermissionRequiredMixin, UserNotifications,
                          CreateView):
    permission_required = ('representantetecnico.add_solicitud',)
    model = Solicitud
    form_class = SolicitudForm
    template_name = "solicitudtl/create.html"
    success_url = reverse_lazy("tl:solicitudes")
    url_redirect = success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Registro solicitudes de entrega sustancias"
        context['icontitle'] = "plus"
        context['url_list'] = self.success_url
        context['action'] = 'add'
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": self.success_url, "uriname": "Solicitudes"},
            {"uridj": reverse_lazy('tl:registrosolicitud'), "uriname": "Registro"}
        ]
        return context

    def get_form_kwargs(self):
        current_laboratory_user = self.request.user.laboratorio_set.first()
        kwargs = super().get_form_kwargs()

        kwargs['initial'] = {
            'proyecto': Proyecto.objects.filter(laboratorio_id=current_laboratory_user.id)
        }
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

                    data['url'] = reverse_lazy('tl:versolicitud', kwargs={'pk': self.object.id})

                else:
                    data['error'] = form.errors

        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data)
