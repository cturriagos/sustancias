from django import forms

from core.representantetecnico.models import Repositorio, TipoRepositorio


class RepositorioCreateFolderForm(forms.ModelForm):
    class Meta:
        model = Repositorio
        fields = ['nombre', 'parent']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'autofocus': True,
                'placeholder': 'Ingrese el nombre de la carpeta'
            })
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                folder = form.save(commit=False)
                folder.is_dir = True
                folder.tipo_repositorio = TipoRepositorio.objects.get(nombre="personal")
                folder.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
