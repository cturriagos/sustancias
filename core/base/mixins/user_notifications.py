from django.db.models import Max
from django.urls import reverse_lazy

from core.base import formaters
from core.representantetecnico.models import ComprasPublicas, Solicitud


class UserNotifications(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notifications'] = []
        context['cant_notifications'] = 0
        if self.request.session['group'].name == 'bodega':
            queryset = ComprasPublicas.objects.filter(bodega__id=self.request.user.bodega_set.first().id,
                                                      estado_compra__estado='registrado')
            if queryset.count() > 0:
                context['notifications'].append({
                    'cant': queryset.count(),
                    'text': 'Compras registradas',
                    'icon': 'fa fa-shopping-cart',
                    'url': "{}{}".format(reverse_lazy('rp:compras'),
                                         "?id={}&action=searchdata&type=est".format(queryset.first().estado_compra_id)),
                    'time': formaters.forma_date_substract_now(queryset.aggregate(max_=Max('date_updated')).get('max_'))
                })

            queryset = Solicitud.objects.filter(bodega_id=self.request.user.bodega_set.first().id,
                                                estado_solicitud__estado='aprobado')
            if queryset.count() > 0:
                context['notifications'].append({
                    'cant': queryset.count(),
                    'text': "Solicitudes aprobadas",
                    'icon': 'fa fa-flask',
                    'url': "{}{}".format(reverse_lazy('tl:solicitudes'), "?id={}&action=searchdata&type=est".format(
                        queryset.first().estado_solicitud_id)),
                    'time': formaters.forma_date_substract_now(queryset.aggregate(max_=Max('date_updated')).get('max_'))
                })
        elif self.request.session['group'].name == 'laboratorio':
            queryset = Solicitud.objects.filter(laboratorio_id=self.request.user.laboratorio_set.first().id,
                                                estado_solicitud__estado='revision')
            if queryset.count() > 0:
                context['notifications'].append({
                    'cant': queryset.count(),
                    'text': 'Solicitudes rechazadas',
                    'icon': 'fa fa-flask',
                    'url': "{}{}".format(reverse_lazy('tl:solicitudes'), "?id={}&action=searchdata&type=est".format(
                        queryset.first().estado_solicitud_id)),
                    'time': formaters.forma_date_substract_now(queryset.aggregate(max_=Max('date_updated')).get('max_'))
                })

            queryset = Solicitud.objects.filter(laboratorio_id=self.request.user.laboratorio_set.first().id,
                                                estado_solicitud__estado='entregado')
            if queryset.count() > 0:
                context['notifications'].append({
                    'cant': queryset.count(),
                    'text': 'Solicitudes por recibir',
                    'icon': 'fa fa-flask',
                    'url': "{}{}".format(reverse_lazy('tl:solicitudes'), "?id={}&action=searchdata&type=est".format(
                        queryset.first().estado_solicitud_id)),
                    'time': formaters.forma_date_substract_now(queryset.aggregate(max_=Max('date_updated')).get('max_'))
                })
        elif self.request.session['group'].name == 'representante':
            queryset = Solicitud.objects.filter(estado_solicitud__estado='registrado')
            if queryset.count() > 0:
                context['notifications'].append({
                    'cant': queryset.count(),
                    'text': 'Solicitudes por aprobar',
                    'icon': 'fa fa-flask',
                    'url': "{}{}".format(reverse_lazy('tl:solicitudes'), "?id={}&action=searchdata&type=est".format(
                        queryset.first().estado_solicitud_id)),
                    'time': formaters.forma_date_substract_now(queryset.aggregate(max_=Max('date_updated')).get('max_'))
                })

            queryset = ComprasPublicas.objects.filter(estado_compra__estado='revision')
            if queryset.count() > 0:
                context['notifications'].append({
                    'cant': queryset.count(),
                    'text': 'Compras rechazadas',
                    'icon': 'fa fa-shopping-cart',
                    'url': "{}{}".format(reverse_lazy('rp:compras'),
                                         "?id={}&action=searchdata&type=est".format(queryset.first().estado_compra_id)),
                    'time': formaters.forma_date_substract_now(queryset.aggregate(max_=Max('date_updated')).get('max_'))
                })

        for notification in context['notifications']:
            context['cant_notifications'] += notification['cant']

        return context
