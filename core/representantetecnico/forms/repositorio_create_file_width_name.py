from django import forms

from core.representantetecnico.models import Repositorio, TipoRepositorio


class RepositorioCreateFileWidthNameForm(forms.ModelForm):
    is_name_file = forms.BooleanField(initial=True)

    def __init__(self, *args, **kwargs):
        if 'type_location' in kwargs:
            self.type_location = kwargs.pop('type_location')

        super().__init__(*args, **kwargs)
        self.fields['documento'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['documento'].required = True
        self.fields['is_name_file'].widget.attrs.update({
            'class': 'form-check-input'
        })
        self.fields['is_name_file'].required = False
        self.fields['nombre'].required = True

    class Meta:
        model = Repositorio
        fields = ['parent', 'documento', 'nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'autofocus': True,
                'disabled': True,
                'placeholder': 'Ingrese el nombre de la carpeta'
            })
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                archivo = form.save(commit=False)

                if self.type_location == 'archgen':
                    archivo.tipo_repositorio = TipoRepositorio.objects.get(nombre="general")
                elif self.type_location == 'archext':
                    archivo.tipo_repositorio = TipoRepositorio.objects.get(nombre="externo")

                archivo.is_file = True
                archivo.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
