from django import forms

from core.login.models import User


class RecuperarUsuarioForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Ingrese su correo electronico',
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        cleaned_data = super().clean()

        if not User.objects.filter(email=cleaned_data['email']).exists():
            raise forms.ValidationError("El correo electronico no existe")

        return cleaned_data

    def get_user(self):
        if self.user:
            return self.user

        email = self.cleaned_data['email']

        self.user = User.objects.get(email=email)

        return self.get_user()
