from django.contrib import admin
from .models import RegistroAsistencia, SesionQR, Justificacion


@admin.register(RegistroAsistencia)
class RegistroAsistenciaAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'curso', 'fecha', 'estado', 'metodo_registro')
    list_filter = ('estado', 'fecha', 'metodo_registro')
    search_fields = ('alumno__first_name', 'alumno__last_name', 'curso__nombre')


@admin.register(SesionQR)
class SesionQRAdmin(admin.ModelAdmin):
    list_display = ('curso', 'docente', 'fecha', 'activa', 'codigo_validacion')
    list_filter = ('activa', 'fecha')


@admin.register(Justificacion)
class JustificacionAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'curso', 'fecha_inicial', 'fecha_final', 'estado')
    list_filter = ('estado',)
    search_fields = ('alumno__first_name', 'alumno__last_name')
