from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView

from app import settings
from core.login.forms.password_reset_form import PasswordResetForm


class PasswordResetView(FormView):
    form_class = PasswordResetForm
    template_name = 'login/user_reset_password.html'
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Reseteo de contraseña"
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = self.get_form()

            if form.is_valid():
                user_for_reset = form.get_user()

                user_for_reset.controller.reset_password(request=request)

            else:
                data['error'] = form.errors

        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data, safe=False)
