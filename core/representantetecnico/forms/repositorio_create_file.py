from django import forms

from core.representantetecnico.models import Repositorio, TipoRepositorio


class RepositorioCreateFileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if 'type_location' in kwargs:
            self.type_location = kwargs.pop('type_location')

        super().__init__(*args, **kwargs)

    class Meta:
        model = Repositorio
        fields = ['parent', 'documento']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                file = form.save(commit=False)
                file.is_file = True
                file.tipo_repositorio = TipoRepositorio.objects.get(nombre="personal")
                file.nombre = file.documento.file.name
                file.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
