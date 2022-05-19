from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins.is_user_ucscsf import IsUserUCSCSF
from core.base.mixins.user_notifications import UserNotifications
from core.login.forms.user_profile_form import UserProfileForm
from core.login.models import User


class UserProfileView(LoginRequiredMixin, IsUserUCSCSF, UserNotifications, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'usuarios/profile.html'
    success_url = reverse_lazy('dashboard')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['icontitle'] = "edit"
        context['url_list'] = self.success_url
        context['action'] = 'edit'
        context['title'] = "Ediccion de perfil"
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": reverse_lazy('session:usuarios'), "uriname": "Perfil"},
        ]

        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')
            if action == 'edit':

                form = self.get_form()

                if form.is_valid():

                    self.object = form.instance

                    self.object.controller.update_profile(request)

                else:
                    data['error'] = form.errors

        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data)
