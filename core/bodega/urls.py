from django.urls import path

from core.bodega.view.bodega.create import BodegaCreateView
from core.bodega.view.bodega.delete import BodegaDeleteView
from core.bodega.view.bodega.list import BodegaListView
from core.bodega.view.bodega.update import BodegaUpdateView
from core.bodega.view.bodega.view import BodegaView
from core.bodega.view.sustancia.create import SustanciaCreateView
from core.bodega.view.sustancia.delete import SustanciaDeleteView
from core.bodega.view.sustancia.list import SustanciaListView
from core.bodega.view.sustancia.update import SustanciaUpdateView
from core.bodega.view.sustancia.view import SustanciaView

app_name = "bdg"

urlpatterns = [
    # bodega
    path('bodegas/', BodegaListView.as_view(), name="bodegas"),
    path('bodegas/registro/', BodegaCreateView.as_view(), name="registrobodega"),
    path('bodegas/update/<int:pk>/', BodegaUpdateView.as_view(), name="actualizacionbodega"),
    path('bodegas/delete/<int:pk>/', BodegaDeleteView.as_view(), name="eliminarbodega"),
    path('bodegas/view/<int:pk>/', BodegaView.as_view(), name="verbodega"),

    # sustancias
    path('sustancias/', SustanciaListView.as_view(), name="sustancias"),
    path('sustancias/registro/', SustanciaCreateView.as_view(), name="registrosustancias"),
    path('sustancias/update/<int:pk>/', SustanciaUpdateView.as_view(), name="actualizacionsustancia"),
    path('sustancias/delete/<int:pk>/', SustanciaDeleteView.as_view(), name="eliminarsustancia"),
    path('sustancias/view/<int:pk>/', SustanciaView.as_view(), name="versustancias"),
]
