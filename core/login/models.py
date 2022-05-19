from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.base import formaters
from core.base.models import BaseModel
from core.login.controller.user_controller import UserController

Group.add_to_class('descripcion', models.CharField(max_length=180, null=True, blank=True))


class User(AbstractUser, BaseModel):
    email = models.EmailField(_('email address'), null=True, blank=True, unique=True)
    cedula = models.CharField(max_length=10, verbose_name="Cedula", unique=True, null=True)
    telefono = models.CharField(max_length=10, verbose_name="Telefono", null=True, blank=True)
    imagen = models.ImageField(upload_to="users/%Y/%m/%d", null=True, blank=True)
    is_pass_update = models.BooleanField(default=False, editable=False)
    is_info_update = models.BooleanField(default=False, editable=False)
    token = models.UUIDField(primary_key=False, editable=False, null=True, blank=True, unique=True)

    date_creation = None

    controller = UserController()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = UserController(instance=self)
        self._imagen = self.imagen

    def __str__(self):
        return self.get_full_name()

    def save(self, *args, **kwargs):
        if self._imagen != self.imagen:
            self.imagen = formaters.compress_image(self.imagen, is_icon=True)
            self._imagen = self.imagen

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        db_table = "auth_user"
        ordering = ["id"]
