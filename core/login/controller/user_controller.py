import random
import string
import uuid

from crum import get_current_request
from django.apps import apps
from django.contrib import messages
from django.contrib.auth import password_validation, logout
from django.core import mail
from django.db import transaction
from django.template.loader import get_template
from django.templatetags.static import static
from django.urls import reverse_lazy

from app import settings
from core.base.decorators import get_model
from core.base.mixins.controller import Controller
from core.representantetecnico.validators import validate_domain_email


class UserController(Controller):
    model_str = "login.User"

    def actualizar_info_usuario(self):
        self.object.is_info_update = True
        self.object.save()

    def _cambiar_clave_usuario(self, request):
        pass1 = request.POST.get('pass')
        pass2 = request.POST.get('pass2')
        code = request.POST.get('codeConfirm')

        if pass1 is None or pass2 is None or code is None:
            raise Exception('Datos incorrectos')

        if validate_domain_email(self.object.email) is None:
            raise Exception(
                "No existe correo registrado valido para este usuario, "
                "pongase en contacto con el administrador del sistema para corregir"
            )

        if pass1 != pass2:
            raise Exception('Las contraseñas no coinciden')

        if code != self.object.codeconfirm:
            raise Exception('Código erroreo')

        with transaction.atomic():
            password_validation.validate_password(pass1, self.object)

            self.object.codeconfirm = None
            self.object.set_password(pass1)
            self.object.is_pass_update = True
            self.object.save()

            template_email = get_template("correo/confirmcorrectpass.html")
            context_pass = {"name": self.object.username,
                            "urllogin": request.build_absolute_uri("/"),
                            "logo": request.build_absolute_uri(
                                static('img/uteq/logoUTEQoriginal1.png'))}
            content_pass = template_email.render(context_pass)
            email_send = mail.EmailMultiAlternatives(
                "Cambio de contraseña",
                "Unidad de control de sustancias catalogadas, sujetas a fizcalización",
                settings.EMAIL_HOST_USER,
                [self.object.email]
            )
            email_send.attach_alternative(content_pass, "text/html")
            res_messages_email = email_send.send()

            if res_messages_email != 1:
                raise Exception(
                    'Ocurrio un error al intentar enviar un correo electronico, '
                    'intentelo mas tarde'
                )

    def cambiar_clave_usuario(self, request):
        pass_act = request.POST.get('passact')

        if pass_act is None:
            raise Exception('Datos incorrectos')

        if validate_domain_email(self.object.email) is None:
            raise Exception(
                "No existe correo registrado valido para este usuario, "
                "pongase en contacto con el administrador del sistema para corregir"
            )
        if self.object.check_password(pass_act) is False:
            raise Exception('La contraseña actual escrita es incorrecta')

        self._cambiar_clave_usuario(request)

    @get_model
    def cambiar_clave_usuario_sin_sesion(self, username, request):
        if self.model.objects.filter(username=username).exists() is False:
            raise Exception(
                "No existe el nombre de usuario registrado, "
                "pongase en contacto con el administrador del sistema para corregir"
            )
        self.object = self.model.objects.get(username=username)

        self._cambiar_clave_usuario(request)

    def create_custom_user(self, request, groups):
        with transaction.atomic():
            username = self._get_new_username(key="")
            if username is None:
                raise Exception(
                    'Ocurrio un error al crear un usuario, '
                    'por favor verifique la información a registrar'
                )

            self.object.is_active = False
            self.object.username = username
            self.object.set_password(self.object.cedula)
            self.object.save()

            if len(groups) > 0:
                email_verified = validate_domain_email(self.object.email)
                if email_verified is None:
                    raise Exception(
                        'Ocurrio un error al crear un usuario, '
                        'correo electronico {} no valido para asignar un usuario. Debe ingresar '
                        'un correo electronico institucional'.format(self.object.email)
                    )

                for g in groups:
                    self.object.groups.add(g)

                self.object.is_active = True

                res_messages_email = self._send_email_new_user(request)
                if res_messages_email != 1:
                    raise Exception(
                        'Ocurrio un error al intentar verificar un correo electronico, '
                        'correo electronico {} no valido'.format(self.object.email)
                    )

                self.object.save()

    def delete_object(self):
        if self.permit_delete() is False:
            raise Exception(
                'No es posible eliminar este registro'
                'Pongase en contacto con el administrador del sistema'
            )
        self.object.delete()

    def enviar_codigo_confirmacion(self, request):
        if validate_domain_email(self.object.email) is None:
            raise Exception(
                "No existe correo registrado valido para este usuario, "
                "pongase en contacto con el administrador del sistema para corregir"
            )
        codeconfirmacion = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
        with transaction.atomic():
            self.object.codeconfirm = codeconfirmacion
            self.object.save()
            template_email = get_template("correo/changePass.html")
            context_pass = {"name": self.object.username,
                            "email_admin": settings.EMAIL_HOST_USER,
                            "codeconfirm": codeconfirmacion,
                            "logo": request.build_absolute_uri(
                                static('img/uteq/logoUTEQoriginal1.png'))}
            content_pass = template_email.render(context_pass)
            email_send = mail.EmailMultiAlternatives(
                "Codigo de confirmación",
                "Unidad de control de sustancias catalogadas, sujetas a fizcalización",
                settings.EMAIL_HOST_USER,
                [self.object.email]
            )
            email_send.attach_alternative(content_pass, "text/html")
            res_messages_email = email_send.send()

            if res_messages_email != 1:
                raise Exception(
                    'Ocurrio un error al intentar enviar un correo electronico, '
                    'intentelo mas tarde'
                )

    @get_model
    def enviar_codigo_confirmacion_sin_sesion(self, username, request):

        if self.model.objects.filter(username=username).exists() is False:
            raise Exception(
                "No existe el nombre de usuario registrado, "
                "pongase en contacto con el administrador del sistema para corregir"
            )
        self.object = self.model.objects.get(username=username)

        self.enviar_codigo_confirmacion(request=request)

    def enviar_usuarios_persona(self, request):
        user_item = {'username': self.object.username, 'estado': ''}

        if self.object.is_active:
            user_item['estado'] = 'Activo'
        else:
            user_item['estado'] = 'Inactivo'

        template_email = get_template("correo/sendUser.html")
        context_pass = {"name": self.object.get_full_name(),
                        "user": user_item,
                        "email_host": settings.EMAIL_HOST_USER,
                        "urllogin": request.build_absolute_uri("/"),
                        "logo": request.build_absolute_uri(
                            static('img/uteq/logoUTEQoriginal1.png'))}
        content_pass = template_email.render(context_pass)
        email_send = mail.EmailMultiAlternatives(
            "Envio de correo",
            "Unidad de control de sustancias catalogadas, sujetas a fizcalización",
            settings.EMAIL_HOST_USER,
            [self.object.email]
        )
        email_send.attach_alternative(content_pass, "text/html")
        emailsend_rest = email_send.send()
        if emailsend_rest != 1:
            raise Exception(
                "ha ocurrido un error al enviar el correo, "
                "por favor vuelva a intentarlo"
            )

    @get_model
    def enviar_usuarios_persona_sin_sesion(self, correo, request):
        if self.model.objects.filter(email=correo).exists() is False:
            raise Exception(
                "No existe este correo registrado, "
                "pongase en contacto con el administrador del sistema para corregir"
            )
        self.object = self.model.objects.get(email=correo)

        self.enviar_usuarios_persona(request)

    def get_choices_all_groups(self):
        group_model = apps.get_model("auth", "Group")
        choices = []
        choices += [(o.id, o.descripcion) for o in group_model.objects.all()]
        return choices

    def get_choices_laboratory_user(self):
        laboratory_model = apps.get_model("tecnicolaboratorio", "Laboratorio")
        choices = [('', '---------')]
        choices += [(o.id, o.nombre) for o in laboratory_model.objects.filter(responsable_id=self.object.id)]
        return choices

    def get_choices_proyecto_laboratory_user(self):
        proyecto_model = apps.get_model("tecnicolaboratorio", "Proyecto")

        current_lab_user = self.object.laboratorio_set.first()

        choices = [('', '---------')]
        choices += [(o.id, o.nombre) for o in proyecto_model.objects.filter(laboratorio_id=current_lab_user.id)]

        return choices

    @get_model
    def get_choices_user_not_superuser(self):
        choices = [('', '---------')]
        choices += [(o.id, o.get_full_name()) for o in self.model.objects.filter(is_superuser=False)]
        return choices

    def get_imagen(self):
        if self.object.imagen:
            return '{}{}'.format(settings.MEDIA_URL, self.object.imagen)
        else:
            return '{}{}'.format(settings.STATIC_URL, 'img/user.png')

    def _get_names_part(self):
        parts = ["", "", "", ""]
        nombre_array = self.object.first_name.strip().split(sep=" ")
        apellido_array = self.object.last_name.strip().split(sep=" ")
        if len(nombre_array) >= 1:
            parts[0] = nombre_array[0]
        if len(nombre_array) >= 2:
            parts[1] = nombre_array[1]
        if len(apellido_array) >= 1:
            parts[2] = apellido_array[0]
        if len(apellido_array) >= 2:
            parts[3] = apellido_array[1]
        return parts

    def _get_new_username(self, key=""):
        parts = self._get_names_part()
        if parts is not None:
            username = parts[0][0:1]
            username += parts[2]
            username += parts[3][0:1]
            username += key
            username = str(username).lower()
            username_temp = username
            count = 0
            while self._username_exists(username):
                count += 1
                username = username_temp + str(count)
            return username
        return None

    def get_user_info(self):
        if self.object is not None:
            return self.object.get_full_name()
        else:
            return ""

    def permit_delete(self):
        if self.object.bodega_set.count() > 0 \
                or self.object.proyecto_set.count() > 0 \
                or self.object.user_creation_representantetecnico_solicitud_set.count() > 0 \
                or self.object.laboratorio_set.count() > 0 \
                or self.object.user_creation_representantetecnico_informesmensuales_set.count() > 0 \
                or self.object.groups.count() > 0:
            return False
        return True

    def reset_password(self, request):
        self.object.token = uuid.uuid4()
        self.object.is_pass_update = False
        self.object.save()

        url_reset = request.build_absolute_uri(
            reverse_lazy('session:cambiar_clave_sin_session', kwargs={'token': self.object.token}))

        template_email = get_template("correo/rest_password.html")
        context_email = {"name": self.object.get_full_name(),
                         "urlreset": url_reset,
                         "logo": request.build_absolute_uri(static('img/uteq/logoUTEQoriginal1.png')),
                         'email_host': settings.EMAIL_HOST_USER
                         }
        content_email = template_email.render(context_email)
        email_send = mail.EmailMultiAlternatives(
            "Reseteo de contraseña",
            "Unidad de control de sustancias catalogadas, sujetas a fizcalización",
            settings.EMAIL_HOST_USER,
            [self.object.email]
        )

        email_send.attach_alternative(content_email, "text/html")
        response = email_send.send()

        if response != 1:
            raise Exception("Ocurrio un error al intentar enviar el correo, intentelo de nuevo")

    @get_model
    def search_data(self, request):
        data = []

        query = self.model.objects.all()

        for per in query:
            if not per.is_superuser and per.id != self.object.id:
                item = {'id': per.id, 'nombre': per.first_name, 'apellido': per.last_name, 'cedula': per.cedula,
                        'email': per.email}

                if request.session['group'].name == 'representante':
                    item['rol'] = [{'id': item.id, 'rol': item.descripcion} for item in per.groups.all()]

                data.append(item)

        return data

    def _send_email_new_user(self, request):
        template_email = get_template("correo/correo.html")
        context_email = {"name": self.object.get_full_name(),
                         "username": self.object.username,
                         "email": self.object.email,
                         "urllogin": request.build_absolute_uri("/"),
                         "logo": request.build_absolute_uri(
                             static('img/uteq/logoUTEQoriginal1.png'))}
        content_email = template_email.render(context_email)
        email_send = mail.EmailMultiAlternatives(
            "Nuevo usuario",
            "Unidad de control de sustancias catalogadas, sujetas a fizcalización",
            settings.EMAIL_HOST_USER,
            [self.object.email]
        )
        email_send.attach_alternative(content_email, "text/html")
        return email_send.send()

    def set_group_session_initial(self):
        request = get_current_request()

        groups = self.object.groups.all()

        errors = []

        if 'group' in request.session:
            request.session.pop('group')

        if groups.exists():

            for group in groups:
                try:
                    self._validate_change_current_group(group, request)
                except Exception as e:
                    errors.append(str(e))

                if 'group' in request.session:
                    break

        if 'group' not in request.session:
            for error in errors:
                messages.error(request, error)

            logout(request)

    def update_password(self, password):
        self.object.set_password(password)
        self.object.is_pass_update = True
        self.object.token = None
        self.object.save()

    @get_model
    def update_profile(self, request):
        with transaction.atomic():
            user_old = self.model.objects.get(pk=self.object.id)
            if self.object.email != user_old.email:
                res_messages_email = self._send_email_new_user(request)
                if res_messages_email != 1:
                    raise Exception(
                        'Ocurrio un error al intentar verificar el correo electronico, '
                        'correo electronico {} no valido'.format(self.object.email)
                    )

            self.object.save()

    @get_model
    def update_user(self, request, groups):
        with transaction.atomic():

            user_old = self.model.objects.get(pk=self.object.id)

            self.object.is_active = False
            self.object.save()

            self.object.groups.clear()

            if len(groups) > 0:
                if self.object.email != user_old.email:
                    email_verified = validate_domain_email(self.object.email)
                    if email_verified is None:
                        raise Exception(
                            'Ocurrio un error al crear un usuario, '
                            'correo electronico {} no valido para asignar un usuario. Debe ingresar '
                            'un correo electronico institucional'.format(self.object.email)
                        )

                for g in groups:
                    self.object.groups.add(g)

                self.object.is_active = True

                if self.object.email != user_old.email:
                    res_messages_email = self._send_email_new_user(request)
                    if res_messages_email != 1:
                        raise Exception(
                            'Ocurrio un error al intentar verificar un correo electronico, '
                            'correo electronico {} no valido'.format(self.object.email)
                        )

                self.object.save()

    @get_model
    def _username_exists(self, username):
        if self.model.objects.filter(username=username).exclude(pk=self.object.id).exists():
            return True
        return False

    def _validate_change_current_group(self, group, request):

        if group.name == 'bodega':
            if self.object.bodega_set.all().count() == 0:
                raise Exception("No tiene bodegas asignadas a este usuario")

        if group.name == 'laboratorio':
            if self.object.laboratorio_set.all().count() == 0:
                raise Exception("No tiene bodegas asignadas a este usuario")

        request.session['group'] = group

    def validate_change_current_group(self, group, request):
        self._validate_change_current_group(group, request)
