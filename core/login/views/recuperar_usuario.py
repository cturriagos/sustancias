from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView

from core.login.controller.user_controller import UserController
from core.login.forms.recuperar_usuario_form import RecuperarUsuarioForm


class RecuperarUser(FormView):
    form_class = RecuperarUsuarioForm
    success_url = reverse_lazy('session:login')
    template_name = "login/recuperar_usuario.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = UserController()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Recuperar nombre de usuario"
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = self.get_form()

            if form.is_valid():
                user_for_send = form.get_user()

                user_for_send.controller.enviar_usuarios_persona(request)

            else:
                data['error'] = form.errors

        except Exception as e:
            data["error"] = str(e)

        return JsonResponse(data, safe=False)
