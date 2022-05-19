from django.urls import path

from core.representantetecnico.views.compras.create import ComprasCreateView
from core.representantetecnico.views.compras.delete import ComprasDeleteView
from core.representantetecnico.views.compras.list import ComprasListView
from core.representantetecnico.views.compras.update import ComprasUpdateView
from core.representantetecnico.views.compras.view import ComprasView
from core.representantetecnico.views.empresa.create import EmpresaCreateView
from core.representantetecnico.views.empresa.delete import EmpresaDeleteView
from core.representantetecnico.views.empresa.list import EmpresaListView
from core.representantetecnico.views.empresa.update import EmpresaUpdateView
from core.representantetecnico.views.empresa.view import EmpresaView
from core.representantetecnico.views.movimientosinventario.estado_mensual import EstadoMensualListView
from core.representantetecnico.views.movimientosinventario.movimientos_mensuales import MovimientosInventarioListView
from core.representantetecnico.views.repositorio.list import RepositorioListView

app_name = "rp"

urlpatterns = [

    # inventario
    path('inventario/', MovimientosInventarioListView.as_view(), name="movimientoinventario"),
    path('inventario/estado-mensual/', EstadoMensualListView.as_view(), name="estadomensual"),

    # compras publicas
    path('compras/', ComprasListView.as_view(), name="compras"),
    path('compras/registro/', ComprasCreateView.as_view(), name="registrocompras"),
    path('compras/update/<int:pk>/', ComprasUpdateView.as_view(), name="actualizacioncompras"),
    path('compras/delete/<int:pk>/', ComprasDeleteView.as_view(), name="eliminarcompras"),
    path('compras/view/<int:pk>/', ComprasView.as_view(), name="vercompras"),

    # empresa
    path('empresas/', EmpresaListView.as_view(), name="empresas"),
    path('empresas/registro/', EmpresaCreateView.as_view(), name="registroempresa"),
    path('empresas/update/<int:pk>/', EmpresaUpdateView.as_view(), name="actualizacionempresa"),
    path('empresas/delete/<int:pk>/', EmpresaDeleteView.as_view(), name="eliminarempresa"),
    path('empresas/view/<int:pk>/', EmpresaView.as_view(), name="verempresa"),

    # repositorio
    path('repositorio/', RepositorioListView.as_view(), name="repositorio"),
    path('repositorio/<int:pk>/', RepositorioListView.as_view(), name="repositorioid"),
]
