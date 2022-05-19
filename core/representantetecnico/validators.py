from django.core.exceptions import ValidationError


# validar campo convocatoria de tabla compras
def validate_compras_convocatoria(value):
    if value > 0:
        return True
    else:
        raise ValidationError("Este campo no puede contener valores negativos")


def validate_domain_email(email):
    email = str(email).strip()
    if email.__contains__("@"):
        domain = email.split('@')[1]
        domain_list = ["uteq.edu.ec", ]
        if domain in domain_list:
            return email
    return None
