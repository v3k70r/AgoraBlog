from django.urls import path
from . import views

urlpatterns = [
    path('', views.publicacion_list, name='publicacion_list'),
    path('publicacion/<int:pk>/', views.publicacion_detail, name='publicacion_detail'),
    path('publicacion/nueva/', views.publicacion_create, name='publicacion_create'),
    path('publicacion/<int:pk>/editar/', views.publicacion_update, name='publicacion_update'),
    path('publicacion/<int:pk>/eliminar/', views.publicacion_delete, name='publicacion_delete'),
]