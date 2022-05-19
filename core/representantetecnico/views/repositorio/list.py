from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from core.base.mixins.is_user_ucscsf import IsUserUCSCSF
from core.base.mixins.user_notifications import UserNotifications
from core.base.mixins.validate_permission_required_mixin import ValidatePermissionRequiredMixin
from core.representantetecnico.forms.repositorio_create_file import RepositorioCreateFileForm
from core.representantetecnico.forms.repositorio_create_file_width_name import RepositorioCreateFileWidthNameForm
from core.representantetecnico.forms.repositorio_create_folder_form import RepositorioCreateFolderForm
from core.representantetecnico.models import Repositorio


class RepositorioListView(LoginRequiredMixin, IsUserUCSCSF, ValidatePermissionRequiredMixin, UserNotifications,
                          TemplateView):
    permission_required = ('representantetecnico.view_repositorio',)
    template_name = "repositorio/list.html"
    url_redirect = reverse_lazy('dashboard')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = Repositorio()

    def dispatch(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            type_filter = request.GET.get('type')

            if pk is not None:
                if self.object is not None and self.object.id != pk:
                    if type_filter in ['repository', 'archgen', 'archext', 'recicle']:
                        self.object = Repositorio.objects.get(pk=pk)

            return super().dispatch(request, *args, **kwargs)

        except Exception as e:
            messages.error(request, str(e))

        return HttpResponseRedirect(self.url_redirect)

    def get(self, request, *args, **kwargs):
        try:
            action = request.GET.get('action')
            if action == 'searchcontent':
                data = self.object.controller.search_content(request)

                return JsonResponse(data, safe=False)

        except Exception as e:
            messages.error(request, str(e))

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formfolder'] = RepositorioCreateFolderForm()
        context['formfile'] = RepositorioCreateFileWidthNameForm()
        context['title'] = "Repositorio"
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')
            kwargs = dict()

            if action == 'newfolder':
                form_folder = RepositorioCreateFolderForm(request.POST, request.FILES, instance=None, initial={
                    'parent': self.object
                })
                data = form_folder.save()
            elif action == 'newfilewidthname':
                form_file_width_name = RepositorioCreateFileWidthNameForm(request.POST, request.FILES, instance=None,
                                                                          type_location=request.POST.get('type'))
                data = form_file_width_name.save()
            elif action == 'createfile':
                form_file = RepositorioCreateFileForm(request.POST, request.FILES, instance=None,
                                                      initial={'parent': self.object})
                data = form_file.save()
            elif action == 'deleteitem':

                self.object.controller.delete_item(request)

            elif action == 'restoreitem':
                kwargs["id_item"] = request.POST.get('id')

                self.object.controller.restore_item(*args, **kwargs)

        except Exception as e:
            data["error"] = str(e)

        return JsonResponse(data, safe=False)
