from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins.is_user_ucscsf import IsUserUCSCSF
from core.base.mixins.user_notifications import UserNotifications
from core.base.mixins.validate_permission_required_mixin import ValidatePermissionRequiredMixin
from core.representantetecnico.models import InformesMensuales


class InformeMensualView(LoginRequiredMixin, IsUserUCSCSF, ValidatePermissionRequiredMixin, UserNotifications,
                         TemplateView):
    permission_required = ('representantetecnico.view_informesmensuales',)
    template_name = 'informesmensuales/view.html'
    url_redirect = reverse_lazy('tl:informesmensuales')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def dispatch(self, request, *args, **kwargs):
        try:
            self.object = InformesMensuales.objects.get(pk=kwargs['pk'])

            return super().dispatch(request, *args, **kwargs)

        except Exception as e:
            messages.error(request, str(e))

        return HttpResponseRedirect(self.url_redirect)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_list'] = self.url_redirect
        context['icontitle'] = 'eye'
        context['title'] = '{} {}'.format("Informe mensual", self.object.id)
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": self.url_redirect, "uriname": "Informes mensuales"},
            {"uridj": reverse_lazy('tl:verinformesmensuales', kwargs={'pk': self.object.id}),
             "uriname": "Informe {}".format(self.object.id)}
        ]
        return context

    def get(self, request, *args, **kwargs):
        try:
            action = request.GET.get('action')

            if action is not None:
                if action == 'informe_detail':
                    data = self.object.controller.get_informe_detail()

                    return JsonResponse(data, safe=False)

        except Exception as e:
            messages.error(request, str(e))

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}

        try:
            action = request.POST.get('action')

            if action == 'archivar_informe':
                self.object.controller.archivar_informe(request)

        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data)
