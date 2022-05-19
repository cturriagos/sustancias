from django.urls import path

from core.login.views.login import LoginFormView
from core.login.views.logout import LogoutRedirectView
from core.login.views.recuperar_usuario import RecuperarUser
from core.login.views.user_change_group import UserChangeGroup
from core.login.views.usuarios.change_password import ChangePasswordView
from core.login.views.usuarios.create import UserCreateView
from core.login.views.usuarios.delete import UserDeleteView
from core.login.views.usuarios.list import UserListView
from core.login.views.usuarios.password_reset import PasswordResetView
from core.login.views.usuarios.profile import UserProfileView
from core.login.views.usuarios.update import UserUpdateView
from core.login.views.usuarios.user_update_password import UserUpdatePasswordView
from core.login.views.usuarios.view import UserView

app_name = "session"

urlpatterns = [
    path('', LoginFormView.as_view(), name="login"),
    path('logout/', LogoutRedirectView.as_view(), name="logout"),
    path('salve/user/', RecuperarUser.as_view(), name="recuperaruser"),
    path('password/reset/', PasswordResetView.as_view(), name="resetpassword"),
    path('change/group/<int:pk>/', UserChangeGroup.as_view(), name='user_change_group'),
    path('change/password/<str:token>/', ChangePasswordView.as_view(), name="cambiar_clave_sin_session"),

    # usuarios
    path('usuarios/', UserListView.as_view(), name="usuarios"),
    path('usuarios/registro/', UserCreateView.as_view(), name="registrousuarios"),
    path('usuarios/update/<int:pk>/', UserUpdateView.as_view(), name="actualizacionusuarios"),
    path('usuarios/delete/<int:pk>/', UserDeleteView.as_view(), name="eliminarususuarios"),
    path('usuarios/view/<int:pk>/', UserView.as_view(), name="verusuarios"),
    path('perfil/', UserProfileView.as_view(), name="perfilusuario"),
    path('perfil/change/password/', UserUpdatePasswordView.as_view(), name="cambiar_clave"),
]
