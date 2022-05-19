from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins.is_user_ucscsf import IsUserUCSCSF
from core.base.mixins.user_notifications import UserNotifications
from core.base.mixins.validate_permission_required_mixin import ValidatePermissionRequiredMixin
from core.login.models import User
from core.login.forms.user_form import UserForm


class UserUpdateView(LoginRequiredMixin, IsUserUCSCSF, ValidatePermissionRequiredMixin, UserNotifications, UpdateView):
    permission_required = ('login.change_user',)
    model = User
    form_class = UserForm
    template_name = 'usuarios/create.html'
    success_url = reverse_lazy('session:usuarios')
    url_redirect = success_url

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def dispatch(self, request, *args, **kwargs):
        try:
            if request.user.id == kwargs['pk']:
                raise Exception("""
                    No puede realizar esta accion,
                    para mas información, consulte con los administradores del sistema
                """)
            self.object = self.get_object()

            return super().dispatch(request, *args, **kwargs)

        except Exception as e:
            messages.error(request, str(e))

        return HttpResponseRedirect(self.url_redirect)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['icontitle'] = "edit"
        context['url_list'] = self.success_url
        context['action'] = 'edit'
        context['title'] = "Personas"
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": reverse_lazy('session:usuarios'), "uriname": "Personas"},
            {"uridj": reverse_lazy('session:actualizacionusuarios', kwargs={'pk': self.object.id}),
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

                    self.object.controller.update_user(request, form.cleaned_data['groups'])

                    data['url'] = reverse_lazy('verusuarios', kwargs={'pk': self.object.id})

                else:
                    data['error'] = form.errors

        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data)
