from django.apps import apps
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class ValidatePermissionRequiredMixin(object):
    permission_required = ''
    url_redirect = None

    def get_perms(self):
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        return perms

    def get_url_redirect(self):
        if self.url_redirect is None:
            return reverse_lazy('session:login')
        else:
            return self.url_redirect

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        if self.has_perms_for_current_group(request.session['group']):
            if request.user.is_pass_update is False:
                messages.error(request, 'Es necesario que cambie su contraseña inicial')
                return HttpResponseRedirect(reverse_lazy('session:cambiar_clave'))

            if request.user.is_info_update is False:
                messages.error(request, 'No ha actualizado su información')
                return HttpResponseRedirect(reverse_lazy('session:perfilusuario'))

            return super().dispatch(request, *args, **kwargs)

        messages.error(request, 'No tiene permiso para entrar a este módulo')
        messages.error(request, 'Pongase en contacto con el administrador del sistema')

        return HttpResponseRedirect(self.get_url_redirect())

    def has_perms_for_current_group(self, current_group):
        permision_model = apps.get_model("auth", "Permission")

        perms = permision_model.objects.filter(group__id=current_group.id)

        perms = perms.values_list('content_type__app_label', 'codename').order_by()

        permisions = {"%s.%s" % (ct, name) for ct, name in perms}

        return all(perm in permisions for perm in self.get_perms())
