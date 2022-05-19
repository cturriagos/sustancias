from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins.is_user_ucscsf import IsUserUCSCSF
from core.base.mixins.user_notifications import UserNotifications
from core.base.mixins.validate_permission_required_mixin import ValidatePermissionRequiredMixin
from core.tecnicolaboratorio.forms.laboratorio_form import LaboratorioForm
from core.tecnicolaboratorio.models import Laboratorio


class LaboratorioUpdateView(LoginRequiredMixin, IsUserUCSCSF, ValidatePermissionRequiredMixin, UserNotifications,
                            UpdateView):
    permission_required = ('tecnicolaboratorio.change_laboratorio',)
    model = Laboratorio
    form_class = LaboratorioForm
    template_name = 'laboratorio/create.html'
    success_url = reverse_lazy('tl:laboratorios')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):

        self.object = self.get_object()

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Actualizar laboratorio"
        context['icontitle'] = "edit"
        context['url_list'] = self.success_url
        context['action'] = 'edit'
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": self.success_url, "uriname": "Laboratorios"},
            {"uridj": reverse_lazy('tl:registrolaboratorio'), "uriname": "Edicción"}
        ]
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']

            if action == 'edit':
                form = self.get_form()

                if form.is_valid():

                    self.object = form.instance
                    self.object.save()

                    data['url'] = reverse_lazy('tl:verlaboratorios', kwargs={'pk': self.object.id})

                else:
                    data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data)
