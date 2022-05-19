from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView

from core.login.forms.change_password_form import PasswordChangeForm
from core.login.models import User


class ChangePasswordView(FormView):
    form_class = PasswordChangeForm
    template_name = "login/change_password.html"
    success_url = reverse_lazy('session:login')

    def get(self, request, *args, **kwargs):
        token = self.kwargs.get('token')

        if token is not None:
            try:
                if User.objects.filter(token=token).exists():
                    return super().get(request, *args, **kwargs)
            except:
                pass

        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Nueva contraseña"
        return context

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['token'] = self.kwargs['token']
        return form_kwargs

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = self.get_form()

            if form.is_valid():

                user = form.get_user()
                user.controller.update_password(form.cleaned_data['password1'])

            else:
                data['error'] = form.errors

        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data, safe=False)
