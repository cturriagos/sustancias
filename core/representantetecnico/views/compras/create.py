import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins.is_user_ucscsf import IsUserUCSCSF
from core.base.mixins.user_notifications import UserNotifications
from core.base.mixins.validate_permission_required_mixin import ValidatePermissionRequiredMixin
from core.representantetecnico.forms.compra_form import ComprasForm
from core.representantetecnico.models import ComprasPublicas


class ComprasCreateView(LoginRequiredMixin, IsUserUCSCSF, ValidatePermissionRequiredMixin, UserNotifications,
                        CreateView):
    # appname.action(add, change, delete, view)_table
    permission_required = ('representantetecnico.add_compraspublicas',)
    model = ComprasPublicas
    form_class = ComprasForm
    template_name = 'compras/create.html'
    success_url = reverse_lazy('rp:compras')
    url_redirect = success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Registrar compra"
        context['icontitle'] = "plus"
        context['url_list'] = self.success_url
        context['action'] = 'add'
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": self.success_url, "uriname": "Compras"},
            {"uridj": reverse_lazy('rp:registrocompras'), "uriname": "Registro"}
        ]
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')

            if action == 'add':
                form = self.get_form()

                if form.is_valid():

                    self.object = form.instance

                    sustancias = json.loads(request.POST['sustancias'])

                    self.object.controller.registrar_compra(sustancias)

                    data['url'] = reverse_lazy('rp:vercompras', kwargs={'pk': self.object.id})

                else:
                    data['error'] = form.errors

        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data, safe=False)
