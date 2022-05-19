from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins.is_user_ucscsf import IsUserUCSCSF
from core.base.mixins.user_notifications import UserNotifications
from core.login.models import User


class UserUpdatePasswordView(LoginRequiredMixin, IsUserUCSCSF, UserNotifications, FormView):
    model = User
    form_class = PasswordChangeForm
    template_name = 'usuarios/password_change.html'
    success_url = reverse_lazy('session:login')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['icontitle'] = "edit"
        context['url_list'] = self.success_url
        context['action'] = 'edit'
        context['title'] = "Ediccion de contraseña"
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": reverse_lazy('session:usuarios'), "uriname": context['title']},
        ]

        return context

    def get_form(self, form_class=None):
        form = PasswordChangeForm(user=self.request.user)

        form.fields['old_password'].widget.attrs.update(
            {'placeholder': "Ingrese su contraseña actual", 'class': 'form-control', 'autofocus': True})

        form.fields['new_password1'].widget.attrs.update(
            {'placeholder': "Ingrese su nueva contraseña", 'class': 'form-control'})

        form.fields['new_password2'].widget.attrs.update(
            {'placeholder': "Repita su neva contraseña", 'class': 'form-control'})

        return form

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')
            if action == 'edit':

                form = PasswordChangeForm(user=request.user, data=request.POST)

                if form.is_valid():

                    form.save()

                    update_session_auth_hash(request=request, user=form.user)

                else:
                    data['error'] = form.errors

        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data)
