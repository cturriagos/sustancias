from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins.is_user_ucscsf import IsUserUCSCSF
from core.base.mixins.pass_request_to_form_view_mixin import PassRequestToFormViewMixin
from core.base.mixins.user_notifications import UserNotifications
from core.base.mixins.validate_permission_required_mixin import ValidatePermissionRequiredMixin
from core.tecnicolaboratorio.forms.proyecto_form import ProyectoForm
from core.tecnicolaboratorio.models import Proyecto


class ProyectoCreateView(LoginRequiredMixin, IsUserUCSCSF, ValidatePermissionRequiredMixin, PassRequestToFormViewMixin,
                         UserNotifications, CreateView):
    permission_required = ('tecnicolaboratorio.add_proyecto',)
    model = Proyecto
    form_class = ProyectoForm
    template_name = "proyectostl/create.html"
    success_url = reverse_lazy("tl:proyectos")
    url_redirect = success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Registro de proyectos"
        context['icontitle'] = "plus"
        context['url_list'] = self.success_url
        context['action'] = 'add'
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": self.success_url, "uriname": "Proyectos"},
            {"uridj": reverse_lazy('rp:registrobodega'), "uriname": "Registro"}
        ]
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')

            if action == 'add':
                form = self.get_form()

                if form.is_valid():

                    self.object = form.instance

                    self.object.controller.create_object(request)

                    data['url'] = reverse_lazy('tl:verproyecto', kwargs={'pk': self.object.id})

                else:
                    data['error'] = form.error

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
