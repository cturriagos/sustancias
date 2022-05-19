from core.base import querysets
from core.base.mixins.controller import Controller


class InventarioController(Controller):
    model_str = "representantetecnico.Inventario"

    @staticmethod
    def search_data_est(request, mes, year):
        if request.session['group'].name == 'laboratorio':
            return querysets.get_data_inventario_mov(request.user.laboratorio_set.first().id, 0, mes, year)
        elif request.session['group'].name == 'bodega':
            return querysets.get_data_inventario_mov(0, request.user.bodega_set.first().id, mes, year)
        elif request.session['group'].name == 'representante':
            return querysets.get_data_inventario_mov(0, 0, mes, year)

        return []

    @staticmethod
    def search_data_mov(request, _type, _year, _id):
        if request.session['group'].name == 'laboratorio':
            if _type == 'todo':
                return querysets.get_mov_inv_tl(user_id=request.user.id, sustancia_id=0, year=0, mes=0)
            elif _type == 'sus':
                return querysets.get_mov_inv_tl(user_id=request.user.id, sustancia_id=_id, year=0, mes=0)
            elif _type == 'year':
                return querysets.get_mov_inv_tl(user_id=request.user.id, sustancia_id=0, year=_year, mes=_id)
        elif request.session['group'].name == 'bodega':
            if _type == 'todo':
                return querysets.get_mov_inv_bdg(user_id=request.user.id, sustancia_id=0, year=0, mes=0)
            elif _type == 'sus':
                return querysets.get_mov_inv_bdg(user_id=request.user.id, sustancia_id=_id, year=0, mes=0)
            elif _type == 'year':
                return querysets.get_mov_inv_bdg(user_id=request.user.id, sustancia_id=0, year=_year, mes=_id)
        elif request.session['group'].name == 'representante':
            if _type == 'todo':
                return querysets.get_mov_inv_rt(sustancia_id=0, year=0, mes=0)
            elif _type == 'sus':
                return querysets.get_mov_inv_rt(sustancia_id=_id, year=0, mes=0)
            elif _type == 'year':
                return querysets.get_mov_inv_rt(sustancia_id=0, year=_year, mes=_id)

        return []

    @staticmethod
    def get_colum_names_for_states_months(array):
        data = []

        if len(array) == 0:
            return data

        row_record = array[0]

        for key, value in row_record.items():
            data.append({'real': key, 'formated': key.replace("_", " ")})

        return data
