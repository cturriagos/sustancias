from django.conf import settings
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

from core.representantetecnico.models import Repositorio


class LoginFormView(LoginView):
    template_name = "login/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        response = super().form_valid(form)

        self.request.user.controller.set_group_session_initial()

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Inicio de sesión"
        context['carousel'] = Repositorio.objects.filter(tipo_repositorio__nombre="externo")
        return context
