from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins.is_user_ucscsf import IsUserUCSCSF
from core.base.mixins.user_notifications import UserNotifications
from core.base.mixins.validate_permission_required_mixin import ValidatePermissionRequiredMixin
from core.login.forms.user_form import UserForm
from core.login.models import User


class UserCreateView(LoginRequiredMixin, IsUserUCSCSF, ValidatePermissionRequiredMixin, UserNotifications, CreateView):
    permission_required = ('login.add_user',)
    model = User
    form_class = UserForm
    template_name = 'usuarios/create.html'
    success_url = reverse_lazy('session:usuarios')
    url_redirect = success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['icontitle'] = "plus"
        context['url_list'] = self.success_url
        context['action'] = 'add'
        context['title'] = "Registrar Personas"
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": reverse_lazy('session:usuarios'), "uriname": "Personas"},
            {"uridj": reverse_lazy('session:registrousuarios'), "uriname": "Registro"}
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

                    self.object.controller.create_custom_user(request, form.cleaned_data['groups'])

                    data['url'] = reverse_lazy('session:verusuarios', kwargs={'pk': self.object.id})

                else:
                    data['error'] = form.errors

        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data, safe=False)
