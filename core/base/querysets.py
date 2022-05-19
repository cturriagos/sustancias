from django.db import connection

from core.base.formaters import dictfetchall


def get_mov_inv_rt(sustancia_id, year, mes):
    """Trae todos los movimientos hechos en todos los laboratorios y bodegas con stock en el sistema
    con opcion a filtrar la informacion por mes, año, y sustancia"""

    with connection.cursor() as cursor:
        cursor.execute(
            "select dil.id, dil.date_creation, dil.can_mov, dil.sustancia, dil.mod_type, dil.mov_type,  "
            "dil.lugar, dil.nombre_lugar, dil.anio, dil.mes from get_mov_inv_rt(%s, %s, %s) dil;",
            [sustancia_id, year, mes])
        data_res = dictfetchall(cursor)

    return data_res


def get_mov_inv_tl(user_id, sustancia_id, year, mes):
    """Trae todos los movimientos de inventario que se hayan hecho en los laboratorios asignados a un
    laboratorista con opcion a filtrar la informacion por mes, año, y sustancia"""

    with connection.cursor() as cursor:
        cursor.execute(
            "select dil.id, dil.date_creation, dil.can_mov, dil.sustancia, dil.mod_type, dil.mov_type,  "
            "dil.lugar, dil.nombre_lugar, dil.anio, dil.mes from get_mov_inv_tl(%s, %s, %s, %s) dil;",
            [user_id, sustancia_id, year, mes])
        data_res = dictfetchall(cursor)

    return data_res


def get_mov_inv_bdg(user_id, sustancia_id, year, mes):
    """Trae todos los movimientos de inventario que se hayan hecho en las bodegas asignadas a un bodeguero
    con opcion a filtrar la informacion por mes, año, y sustancia"""

    with connection.cursor() as cursor:
        cursor.execute(
            "select dil.id, dil.date_creation, dil.can_mov, dil.sustancia, dil.mod_type, dil.mov_type,  "
            "dil.lugar, dil.nombre_lugar, dil.anio, dil.mes from get_mov_inv_bdg(%s, %s, %s, %s) dil;",
            [user_id, sustancia_id, year, mes])
        data_res = dictfetchall(cursor)
    return data_res


def get_years_disp_inv():
    with connection.cursor() as cursor:
        cursor.execute(
            "select distinct anio from get_data_inventario();")
        data_res = dictfetchall(cursor)
    return data_res


def get_data_inventario_mov(laboratorio_id, bodega_id, mes, year):
    with connection.cursor() as cursor:
        cursor.execute("select * from reporte_mensual(%s, %s, %s, %s) as q1;",
                       [mes, year, laboratorio_id, bodega_id])
        data_res = cursor.fetchone()
    return data_res[0]


def get_cupo_consumido(year, sustancia_id):
    """Trae el cupo consumido de una sustnacia en un año"""
    with connection.cursor() as cursor:
        cursor.execute("select get_cupo_consumido(%s, %s) as suma;", [year, sustancia_id])
        data_res = cursor.fetchone()
    return float(data_res[0])


def get_substances_solicitud(code_lab, code_bod, term):
    """Trae las sustnacias disponibles para una solicitud"""
    with connection.cursor() as cursor:
        cursor.execute("select * from get_substances_solicitud(%s, %s, %s);", [code_lab, code_bod, term])
        data_res = dictfetchall(cursor)
    return data_res


def exist_rows_inventario(year, month):
    """Trae el cupo consumido de una sustnacia en un año"""
    with connection.cursor() as cursor:
        cursor.execute("select count(*) from get_data_inventario() as gdi where gdi.anio=%s and gdi.mes=%s;",
                       [year, month])
        data_res = cursor.fetchone()
    return data_res[0] > 0
