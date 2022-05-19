from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins.is_user_ucscsf import IsUserUCSCSF
from core.base.mixins.user_notifications import UserNotifications
from core.base.mixins.validate_permission_required_mixin import ValidatePermissionRequiredMixin
from core.tecnicolaboratorio.models import Proyecto


class ProyectoListView(LoginRequiredMixin, IsUserUCSCSF, ValidatePermissionRequiredMixin, UserNotifications, ListView):
    permission_required = ('tecnicolaboratorio.view_proyecto',)
    model = Proyecto
    template_name = "proyectostl/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Proyectos registrados"
        context['icontitle'] = "plus"
        context['users_creators'] = ['representante', 'laboratorio']
        context['action'] = 'add'
        context['create_url'] = reverse_lazy('tl:registroproyecto')
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": reverse_lazy('tl:proyectos'), "uriname": "Proyectos"},
        ]
        return context

    def get(self, request, *args, **kwargs):
        try:
            action = request.GET.get('action')
            result = request.GET.get('result')

            if action == 'searchdata' and result == 'jsondata':
                data = self.model.controller.search_data(request)

                return JsonResponse(data, safe=False)

        except Exception as e:
            messages.error(request, str(e))

        return super().get(request, *args, **kwargs)
