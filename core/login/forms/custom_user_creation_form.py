from django.contrib.auth.forms import UserCreationForm

from core.login.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
