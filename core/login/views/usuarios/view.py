from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins.is_user_ucscsf import IsUserUCSCSF
from core.base.mixins.user_notifications import UserNotifications
from core.base.mixins.validate_permission_required_mixin import ValidatePermissionRequiredMixin
from core.login.models import User


class UserView(LoginRequiredMixin, IsUserUCSCSF, ValidatePermissionRequiredMixin, UserNotifications, TemplateView):
    permission_required = ('login.view_user',)
    template_name = 'usuarios/view.html'
    url_redirect = reverse_lazy('session:usuarios')

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

            self.object = User.objects.get(pk=kwargs['pk'])

            return super().dispatch(request, *args, **kwargs)

        except Exception as e:
            messages.error(request, str(e))

        return HttpResponseRedirect(self.url_redirect)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_list'] = self.url_redirect
        context['icontitle'] = 'eye'
        context['is_del'] = self.object.controller.permit_delete()
        context['is_user'] = False
        context['title'] = '{} {}'.format("Persona", self.object.id)
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": self.url_redirect, "uriname": "Personas"},
            {"uridj": reverse_lazy('session:verusuarios', kwargs={'pk': self.object.id}), "uriname": context['title']}
        ]

        if self.object.groups.all().exists():
            context['is_user'] = True

        return context
