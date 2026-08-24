from django.urls import path
from . import views

app_name = 'asistencia'

urlpatterns = [
    path('registrar/', views.registrar_asistencia_manual, name='registrar_asistencia'),
    path('historial/', views.historial_asistencias, name='historial_asistencias'),
    path('mis-asistencias/', views.mis_asistencias, name='mis_asistencias'),

    path('qr/crear/', views.crear_sesion_qr, name='crear_sesion_qr'),
    path('qr/detalle/<int:pk>/', views.detalle_sesion_qr, name='detalle_sesion_qr'),
    path('qr/cerrar/<int:pk>/', views.cerrar_sesion_qr, name='cerrar_sesion_qr'),
    path('qr/escanear/', views.escanear_qr, name='escanear_qr'),
    path('qr/escanear-camara/', views.escanear_qr_camara, name='escanear_qr_camara'),
    path('qr/validar-ajax/', views.validar_qr_ajax, name='validar_qr_ajax'),

    path('justificaciones/', views.lista_justificaciones, name='lista_justificaciones'),
    path('justificaciones/crear/', views.crear_justificacion, name='crear_justificacion'),
    path('justificaciones/<int:pk>/responder/', views.responder_justificacion, name='responder_justificacion'),
]
