from django.urls import path
from . import views
from .views import consultar_destino

urlpatterns = [
    path('', consultar_destino, name='consultar_destino'),
    path('historial/', views.historial_consultas, name='historial_consultas'),
    path('exportar-pdf/', views.exportar_pdf, name='exportar_pdf'),
    path('enviar-email/', views.enviar_historial_email, name='enviar_historial_email'),
]