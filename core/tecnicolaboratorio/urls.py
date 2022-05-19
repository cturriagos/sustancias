from django.urls import path

from core.tecnicolaboratorio.views.desglose_sustancia_informe_mensual.create import \
    DesgloseSustanciaInformeMensualCreateView
from core.tecnicolaboratorio.views.desglose_sustancia_informe_mensual.delete import \
    DesgloseSustanciaInformeMensualDeleteView
from core.tecnicolaboratorio.views.desglose_sustancia_informe_mensual.list import \
    DesgloseSustanciaInformeMensualListView
from core.tecnicolaboratorio.views.informes_mensuales.create import InformesMensualesCreateView
from core.tecnicolaboratorio.views.informes_mensuales.delete import InformesMensualesDeleteView
from core.tecnicolaboratorio.views.informes_mensuales.list import InformesMensualesListView
from core.tecnicolaboratorio.views.informes_mensuales.update import InformesMensualesUpdateView
from core.tecnicolaboratorio.views.informes_mensuales.view import InformeMensualView
from core.tecnicolaboratorio.views.laboratorio.create import LaboratorioCreateView
from core.tecnicolaboratorio.views.laboratorio.delete import LaboratorioDeleteView
from core.tecnicolaboratorio.views.laboratorio.list import LaboratorioListView
from core.tecnicolaboratorio.views.laboratorio.update import LaboratorioUpdateView
from core.tecnicolaboratorio.views.laboratorio.view import LaboratorioView
from core.tecnicolaboratorio.views.proyectos.create import ProyectoCreateView
from core.tecnicolaboratorio.views.proyectos.delete import ProyectoDeleteView
from core.tecnicolaboratorio.views.proyectos.list import ProyectoListView
from core.tecnicolaboratorio.views.proyectos.update import ProyectoUpdateView
from core.tecnicolaboratorio.views.proyectos.view import ProyectoView
from core.tecnicolaboratorio.views.solicitudes.create import SolicitudCreateView
from core.tecnicolaboratorio.views.solicitudes.delete import SolicitudDeleteView
from core.tecnicolaboratorio.views.solicitudes.list import SolicitudListView
from core.tecnicolaboratorio.views.solicitudes.update import SolicitudUpdateView
from core.tecnicolaboratorio.views.solicitudes.view import SolicitudView

app_name = "tl"

urlpatterns = [
    # solicitudes
    path('solicitudes/', SolicitudListView.as_view(), name="solicitudes"),
    path('solicitudes/registro/', SolicitudCreateView.as_view(), name="registrosolicitud"),
    path('solicitudes/update/<int:pk>/', SolicitudUpdateView.as_view(), name="actualizacionsolicitud"),
    path('solicitudes/delete/<int:pk>/', SolicitudDeleteView.as_view(), name="eliminarsolicitud"),
    path('solicitudes/view/<int:pk>/', SolicitudView.as_view(), name="versolicitud"),

    # informes mensuales
    path('informes-mensuales/', InformesMensualesListView.as_view(), name="informesmensuales"),
    path('informes-mensuales/registro/', InformesMensualesCreateView.as_view(), name="registroinformesmensuales"),
    path('informes-mensuales/update/<int:pk>/', InformesMensualesUpdateView.as_view(),
         name="actualizacioninformesmensuales"),
    path('informes-mensuales/delete/<int:pk>/', InformesMensualesDeleteView.as_view(),
         name="eliminarinformesmensuales"),
    path('informes-mensuales/view/<int:pk>/', InformeMensualView.as_view(), name="verinformesmensuales"),

    # informes mensuales desglose
    path('informes-mensuales/desglose-sustancia/', DesgloseSustanciaInformeMensualListView.as_view(),
         name="informesmensualesdesglose"),
    path('informes-mensuales/desglose-sustancia/registro/', DesgloseSustanciaInformeMensualCreateView.as_view(),
         name="registroinformesmensualesdesglose"),
    path('informes-mensuales/desglose-sustancia/delete/<int:pk>/', DesgloseSustanciaInformeMensualDeleteView.as_view(),
         name="eliminarinformesmensualesdesglose"),

    # proyectos
    path('proyectos/', ProyectoListView.as_view(), name="proyectos"),
    path('proyectos/registro/', ProyectoCreateView.as_view(), name="registroproyecto"),
    path('proyectos/update/<int:pk>/', ProyectoUpdateView.as_view(), name="actualizacionproyecto"),
    path('proyectos/delete/<int:pk>/', ProyectoDeleteView.as_view(), name="eliminarproyecto"),
    path('proyectos/view/<int:pk>/', ProyectoView.as_view(), name="verproyecto"),

    # laboratorio
    path('laboratorios/', LaboratorioListView.as_view(), name="laboratorios"),
    path('laboratorios/registro/', LaboratorioCreateView.as_view(), name="registrolaboratorio"),
    path('laboratorios/update/<int:pk>/', LaboratorioUpdateView.as_view(), name="actualizacionlaboratorios"),
    path('laboratorios/delete/<int:pk>/', LaboratorioDeleteView.as_view(), name="eliminarlaboratorio"),
    path('laboratorios/view/<int:pk>/', LaboratorioView.as_view(), name="verlaboratorios"),
]
