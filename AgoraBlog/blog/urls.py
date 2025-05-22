from django.urls import path
from . import views

urlpatterns = [
    path('', views.publicacion_list, name='home'),
path('', views.publicacion_list, name='publicacion_list'),
    path('<int:pk>/', views.publicacion_detail, name='publicacion_detail'),
    path('nueva/', views.publicacion_create, name='publicacion_create'),
    path('<int:pk>/editar/', views.publicacion_update, name='publicacion_update'),
    path('<int:pk>/eliminar/', views.publicacion_delete, name='publicacion_delete'),
]