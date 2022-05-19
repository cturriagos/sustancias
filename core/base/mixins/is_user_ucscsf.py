from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect


class IsUserUCSCSF(object):

    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.all().count() >= 1:
            return super().dispatch(request, *args, **kwargs)
        logout(request)
        messages.error(request, 'Usuario no tiene permiso para entrar al sistema')
        messages.error(request, 'Pongase en contacto con el administrador del sistema')
        return redirect('session:login')
