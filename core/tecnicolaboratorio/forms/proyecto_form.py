from datetime import datetime

from django.forms import *

from core.tecnicolaboratorio.models import Proyecto


class ProyectoForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

        self.fields.get('responsable').choices = self.request.user.controller.get_choices_user_not_superuser()

        if self.request.session['group'].name != 'representante':
            self.Meta.exclude.append('laboratorio')
            if 'laboratorio' in self.fields:
                self.fields.pop('laboratorio')

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get("fecha_inicio")
        fecha_fin = cleaned_data.get("fecha_fin")

        if fecha_fin < fecha_inicio:
            raise ValidationError(
                "La fecha de fin debe ser superior a la fecha de inicio"
            )

        return cleaned_data

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
        model = Proyecto
        fields = '__all__'
        exclude = []
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre del proyecto',
                    'type': 'text',
                    'class': 'form-control',
                    'autocomplete': 'off'
                }
            ),
            'descripcion': Textarea(attrs={
                'class': 'form-control',
                'rows': "5"
            }),
            'tipo_actividad': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'laboratorio': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'responsable': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'fecha_inicio': DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control',
                'type': 'date',
                'autocomplete': 'off',
                'value': datetime.now().strftime('%Y-%m-%d')
            }),
            'fecha_fin': DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control',
                'type': 'date',
                'autocomplete': 'off',
                'value': datetime.now().strftime('%Y-%m-%d')
            })
        }
