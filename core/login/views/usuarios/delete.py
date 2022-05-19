from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins.is_user_ucscsf import IsUserUCSCSF
from core.base.mixins.user_notifications import UserNotifications
from core.base.mixins.validate_permission_required_mixin import ValidatePermissionRequiredMixin
from core.login.models import User


class UserDeleteView(LoginRequiredMixin, IsUserUCSCSF, ValidatePermissionRequiredMixin, UserNotifications, DeleteView):
    permission_required = ('login.delete_user',)
    model = User
    template_name = 'delete.html'
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

            if self.object.controller.permit_delete() is False:
                raise Exception("""
                    No es posible eliminar este registro,
                    Pongase en contacto con el administrador del sistema
                """)

            return super().dispatch(request, *args, **kwargs)

        except Exception as e:
            messages.error(request, str(e))

        return HttpResponseRedirect(self.success_url)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.controller.delete_object()

        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['icontitle'] = "trash-alt"
        context['url_list'] = self.success_url
        context['title'] = "Eliminar Personas"
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": reverse_lazy('session:usuarios'), "uriname": "Personas"},
            {"uridj": reverse_lazy('session:eliminarususuarios', kwargs={'pk': self.object.id}), "uriname": "Eliminar"}
        ]

        return context
