from django.forms import *

from core.representantetecnico.models import InformesMensuales


class InformeMensualForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mes'].empty_label = None

    class Meta:
        model = InformesMensuales
        fields = '__all__'
        exclude = ['laboratorio', 'estado_informe']
        widgets = {
            'mes': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'year': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Año'
            })
        }

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
