from datetime import datetime

from django import forms
from core.representantetecnico.models import Mes


class EstadoMensualFiltrosForm(forms.Form):
    year = forms.IntegerField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'value': datetime.now().year
    }))

    mes = forms.ModelChoiceField(queryset=Mes.objects.all(), empty_label=None, widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))
