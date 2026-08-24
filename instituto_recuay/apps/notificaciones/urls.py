from django.urls import path
from . import views

app_name = 'notificaciones'

urlpatterns = [
    path('', views.lista_notificaciones, name='lista_notificaciones'),
    path('<int:pk>/leida/', views.marcar_leida, name='marcar_leida'),
    path('todas-leidas/', views.marcar_todas_leidas, name='marcar_todas_leidas'),
]
