from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    path('asistencias/excel/', views.reporte_asistencias_excel, name='reporte_asistencias_excel'),
    path('asistencias/pdf/', views.reporte_asistencias_pdf, name='reporte_asistencias_pdf'),
    path('estadistico/', views.reporte_estadistico, name='reporte_estadistico'),
    path('qr/<int:pk>/', views.generar_qr_alumno, name='generar_qr_alumno'),
    path('qr/masivo/', views.generar_qr_masivo, name='generar_qr_masivo'),
]
