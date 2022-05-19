from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView

from core.base.mixins.is_user_ucscsf import IsUserUCSCSF
from core.base.mixins.validate_permission_required_mixin import ValidatePermissionRequiredMixin
from core.representantetecnico.models import DesgloseInfomeMensualDetalle
from core.tecnicolaboratorio.forms.desglose_sustancia_informe_mensual_form import DesgloseSustanciaInformeMensualForm


class DesgloseSustanciaInformeMensualCreateView(LoginRequiredMixin, IsUserUCSCSF, ValidatePermissionRequiredMixin,
                                                CreateView):
    permission_required = ('representantetecnico.add_desgloseinfomemensualdetalle',)
    model = DesgloseInfomeMensualDetalle
    form_class = DesgloseSustanciaInformeMensualForm
    template_name = "desglosesustanciainformemensual/create.html"
    success_url = reverse_lazy("tl:informesmensuales")
    url_redirect = success_url

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')

            if action == 'add':
                form = self.get_form()

                if form.is_valid():

                    self.object = form.instance

                    id_detalle = int(request.POST.get('id_detalle'))

                    self.object.controller.create_object(id_detalle)
                else:
                    data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data)
