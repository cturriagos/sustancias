from django.forms import *

from core.bodega.models import Bodega


class BodegaForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")

        super().__init__(*args, **kwargs)

        self.fields.get('responsable').choices = self.request.user.controller.get_choices_user_not_superuser()

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

    class Meta:
        model = Bodega
        fields = '__all__'
        widgets = {
            'nombre': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre de la bodega',
                'autofocus': True
            }),
            'descripcion': Textarea(attrs={
                'class': 'form-control',
                'rows': "5"
            }),
            'direccion': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre de la empresa'
            }),
            'responsable': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
        }
