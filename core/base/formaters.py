from io import BytesIO

from PIL import Image, ExifTags
from django.core.files import File
from django.utils import formats, datetime_safe, timezone


def dictfetchall(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def format_datetime(value, is_date=True, is_time=True):
    """retorna un valor formateado en formato fecha hora"""
    if value is None:
        return ''

    if is_date and is_time:
        formater = formats.get_format('DATETIME_INPUT_FORMATS')[0]
    elif is_date and is_time is False:
        formater = formats.get_format('DATE_INPUT_FORMATS')[0]
    elif is_date is False and is_time:
        formater = formats.get_format('TIME_INPUT_FORMATS')[0]
    else:
        raise Exception('Valores de fecha y hora desabilitados para formatear')

    if hasattr(value, 'strftime'):
        value = datetime_safe.new_datetime(value)
        return value.strftime(formater)

    return value


def forma_date_substract_now(date_old):
    if not date_old:
        return ""

    date_dif = timezone.now() - date_old
    seconds = date_dif.seconds
    minutes = int(seconds / 60)
    hours = int(minutes / 60)  # Returns number of hours between dates
    days = date_dif.days
    weeks = int(days / 7)  # number of weeks between dates
    months = int(weeks / 4)
    years = int(months / 12)

    if years > 0:
        return "{} año{}".format(years, "s" if years > 1 else "")
    elif months > 0:
        return "{} mes{}".format(months, "es" if months > 1 else "")
    elif weeks > 0:
        return "{} semana{}".format(weeks, "s" if weeks > 1 else "")
    elif days > 0:
        return "{} dia{}".format(days, "s" if days > 1 else "")
    elif hours > 0:
        return "{} hora{}".format(hours, "s" if hours > 1 else "")
    elif minutes > 0:
        return "{} minuto{}".format(minutes, "s" if minutes > 1 else "")
    elif seconds > 0:
        return "{} segundo{}".format(seconds, "s" if seconds > 1 else "")

    return "reciente"


def compress_image(image, is_icon=False, tam_icon=(50, 50)):
    im = Image.open(image)
    # create a BytesIO object
    im_io = BytesIO()
    # si es icono le doy un tamaño pequeño
    if is_icon:
        new_img = tam_icon
        im.thumbnail(new_img)

    # roto la imagen en caso de ser necesario
    im = _fix_image_rotation(im)

    # save image to BytesIO object
    im.save(im_io, 'JPEG', quality=70, optimize=True)
    # create a Django-friendly Files object
    new_image = File(im_io, name=image.name)
    return new_image


def _get_exif_from_image(image):
    exif = {}

    if hasattr(image, '_getexif'):  # only jpegs have _getexif
        exif_or_none = image._getexif()
        if exif_or_none is not None:
            exif = exif_or_none

    return exif


def _get_orientation_from_exif(exif):
    _ORIENTATION_TAG = 'Orientation'
    orientation_iterator = (
        exif.get(tag_key) for tag_key, tag_value in ExifTags.TAGS.items()
        if tag_value == _ORIENTATION_TAG
    )
    orientation = next(orientation_iterator, None)
    return orientation


def _fix_image_rotation(image):
    orientation_to_rotation_map = {
        3: Image.ROTATE_180,
        6: Image.ROTATE_270,
        8: Image.ROTATE_90,
    }
    try:
        exif = _get_exif_from_image(image)
        orientation = _get_orientation_from_exif(exif)
        rotation = orientation_to_rotation_map.get(orientation)
        if rotation:
            image = image.transpose(rotation)

    except Exception as e:
        pass

    finally:
        return image
