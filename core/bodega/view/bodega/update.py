from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins.is_user_ucscsf import IsUserUCSCSF
from core.base.mixins.pass_request_to_form_view_mixin import PassRequestToFormViewMixin
from core.base.mixins.user_notifications import UserNotifications
from core.base.mixins.validate_permission_required_mixin import ValidatePermissionRequiredMixin
from core.bodega.models import Bodega
from core.bodega.forms.bodega_form import BodegaForm


class BodegaUpdateView(LoginRequiredMixin, IsUserUCSCSF, ValidatePermissionRequiredMixin, PassRequestToFormViewMixin,
                       UserNotifications, UpdateView):
    permission_required = ('bodega.change_bodega',)
    model = Bodega
    form_class = BodegaForm
    template_name = 'bodega/create.html'
    success_url = reverse_lazy('bdg:bodegas')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Actualizar datos de bodega"
        context['icontitle'] = "edit"
        context['url_list'] = self.success_url
        context['action'] = 'edit'
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": self.success_url, "uriname": "Bodega"},
            {"uridj": reverse_lazy('bdg:actualizacionbodega', kwargs={'pk': self.object.id}), "uriname": "Edicción"}
        ]
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()

                data = form.save()

                data['url'] = reverse_lazy('bdg:verbodega', kwargs={'pk': self.object.id})

        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data)
