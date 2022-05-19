from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import View

from core.base.mixins.is_user_ucscsf import IsUserUCSCSF


class UserChangeGroup(LoginRequiredMixin, IsUserUCSCSF, View):

    def get(self, request, *args, **kwargs):
        try:
            group = Group.objects.get(pk=self.kwargs['pk'])

            request.user.controller.validate_change_current_group(group, request)

        except Exception as e:
            messages.error(request, str(e))

        return HttpResponseRedirect(reverse_lazy('dashboard'))
