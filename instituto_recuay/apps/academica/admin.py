from django.contrib import admin
from .models import Carrera, Ciclo, Curso, Horario, AsignacionDocente, InscripcionAlumno, ToleranciaConfig


@admin.register(Carrera)
class CarreraAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'duracion_semestres', 'activa')
    list_filter = ('activa',)
    search_fields = ('nombre', 'codigo')


@admin.register(Ciclo)
class CicloAdmin(admin.ModelAdmin):
    list_display = ('carrera', 'numero', 'semestre', 'anio', 'activo')
    list_filter = ('carrera', 'semestre', 'anio', 'activo')


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'ciclo', 'creditos', 'activo')
    list_filter = ('ciclo', 'activo')
    search_fields = ('nombre', 'codigo')


@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ('curso', 'dia', 'hora_inicio', 'hora_fin', 'aula')
    list_filter = ('dia', 'curso')


@admin.register(AsignacionDocente)
class AsignacionDocenteAdmin(admin.ModelAdmin):
    list_display = ('docente', 'curso', 'activa')
    list_filter = ('activa',)


@admin.register(InscripcionAlumno)
class InscripcionAlumnoAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'curso', 'ciclo', 'activa')
    list_filter = ('ciclo', 'activa')


@admin.register(ToleranciaConfig)
class ToleranciaConfigAdmin(admin.ModelAdmin):
    list_display = ('curso', 'docente', 'minutos_tolerancia', 'porcentaje_asistencia_aprobar')
