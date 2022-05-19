from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins.is_user_ucscsf import IsUserUCSCSF
from core.base.mixins.user_notifications import UserNotifications
from core.base.mixins.validate_permission_required_mixin import ValidatePermissionRequiredMixin
from core.representantetecnico.models import Solicitud


class SolicitudView(LoginRequiredMixin, IsUserUCSCSF, ValidatePermissionRequiredMixin, UserNotifications, TemplateView):
    permission_required = ('representantetecnico.view_solicitud',)
    template_name = 'solicitudtl/view.html'
    url_redirect = reverse_lazy('tl:solicitudes')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def dispatch(self, request, *args, **kwargs):
        try:
            self.object = Solicitud.objects.get(pk=kwargs['pk'])

            return super().dispatch(request, *args, **kwargs)

        except Exception as e:
            messages.error(request, str(e))

        return HttpResponseRedirect(self.url_redirect)

    def get(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.GET.get('action')

            if action == 'search_detalle':
                data = self.object.controller.search_detalle()

                return JsonResponse(data, safe=False)

        except Exception as e:
            data['error'] = str(e)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_list'] = self.url_redirect
        context['icontitle'] = 'eye'
        context['title'] = '{} {}'.format("Solicitud", self.object.id)
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": self.url_redirect, "uriname": "Solicitudes"},
            {"uridj": reverse_lazy('tl:versolicitud', kwargs={'pk': self.object.id}),
             "uriname": "Solicitud {}".format(self.object.id)}
        ]
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')

            if action == 'recibirSolicitud':
                if request.session['group'].name == 'laboratorio':
                    self.object.controller.recibir_solicitud()
                else:
                    data['error'] = 'No tiene permisos'

            elif action == 'aprobarSolicitud':
                tipoobs = request.POST.get("tipoobs")
                observacion = request.POST.get('observacion')

                if request.session['group'].name == 'representante':
                    self.object.controller.aprobar_solicitud(tipoobs, observacion)
                else:
                    data['error'] = 'No tiene permisos'

            elif action == 'revisionSolicitud':
                tipoobs = request.POST.get("tipoobs")
                observacion = request.POST.get('observacion')

                if request.session['group'].name == 'representante' or request.session['group'].name == 'bodega':
                    self.object.controller.revision_solicitud(tipoobs, observacion)
                else:
                    data['error'] = 'No tiene permisos'

            elif action == 'entregarSolicitud':
                detalle_solicitud = request.POST.get('detalles')
                observacion_solicitud = request.POST.get('observacion')

                if request.session['group'].name == 'bodega':
                    self.object.controller.entregar_solicitud(detalle_solicitud, observacion_solicitud)
                else:
                    data['error'] = 'No tiene permisos'

        except Exception as e:
            data["error"] = str(e)

        return JsonResponse(data, safe=False)
