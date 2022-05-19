from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from core.base.mixins.is_user_ucscsf import IsUserUCSCSF
from core.base.mixins.user_notifications import UserNotifications
from core.representantetecnico.models import Repositorio


class DashBoard(LoginRequiredMixin, IsUserUCSCSF, UserNotifications, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Dashboard"
        context['carousel'] = Repositorio.objects.filter(tipo_repositorio__nombre="general")
        return context
