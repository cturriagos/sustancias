from django import forms

from core.representantetecnico.models import Solicitud


class SolicitudForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bodega'].empty_label = None

    class Meta:
        model = Solicitud
        fields = '__all__'
        exclude = ['estado_solicitud', 'fecha_autorizacion', 'observacion_representante', 'observacion_bodega',
                   'laboratorio']
        widgets = {
            'proyecto': forms.Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'bodega': forms.Select(attrs={
                'class': 'form-control',
                'style': 'width: 100%'
            }),
            'codigo_solicitud': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese el codigo de la solicitud',
                    'type': 'text',
                    'class': 'form-control',
                    'autocomplete': 'off'
                }
            ),
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
