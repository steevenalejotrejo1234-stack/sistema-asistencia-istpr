from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('lista/', views.lista_usuarios, name='lista_usuarios'),
    path('crear/', views.crear_usuario, name='crear_usuario'),
    path('<int:pk>/editar/', views.editar_usuario, name='editar_usuario'),
    path('<int:pk>/eliminar/', views.eliminar_usuario, name='eliminar_usuario'),
    path('<int:pk>/perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('mi-perfil/', views.mi_perfil, name='mi_perfil'),
    path('cambiar-password/', views.cambiar_password, name='cambiar_password'),
]
