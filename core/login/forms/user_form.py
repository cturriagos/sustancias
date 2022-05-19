from django import forms

from core.login.models import User


class UserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['imagen'].widget.attrs['class'] = ' form-control'
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields.get('groups').choices = self.instance.controller.get_choices_all_groups()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'cedula', 'email', 'telefono', 'imagen', 'groups']
        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff',
                   'is_info_update', 'is_pass_update', 'username', 'password']
        labels = {
            'groups': "Usuarios",
            'first_name': "Nombres"
        }
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese los nombres',
                    'type': 'text',
                    'class': 'form-control',
                    'autocomplete': 'off'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese los apellidos',
                    'type': 'text',
                    'class': 'form-control',
                    'autocomplete': 'off'
                }
            ),
            'cedula': forms.NumberInput(
                attrs={
                    'placeholder': 'Ingrese el numero de cedula',
                    'type': 'text',
                    'minlength': 10,
                    'onkeypress': 'return event.charCode >= 48 && event.charCode <= 57',
                    'class': 'form-control',
                    'autocomplete': 'off'
                }
            ),
            'telefono': forms.NumberInput(
                attrs={
                    'placeholder': 'Ingrese el numero de telefono',
                    'type': 'text',
                    'minlength': 10,
                    'onkeypress': 'return event.charCode >= 48 && event.charCode <= 57',
                    'class': 'form-control',
                    'autocomplete': 'off'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Ingrese el correo electronico',
                    'class': 'form-control',
                    'autocomplete': 'off',
                    'type': 'email'
                }
            ),
            'groups': forms.SelectMultiple(attrs={
                'class': 'form-control select2-multiple',
                'style': 'width: 100%',
                'multiple': 'multiple'
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
