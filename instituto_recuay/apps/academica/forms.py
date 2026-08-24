from django import forms
from .models import Carrera, Ciclo, Curso, Horario, AsignacionDocente, InscripcionAlumno, ToleranciaConfig


class CarreraForm(forms.ModelForm):
    class Meta:
        model = Carrera
        fields = ('nombre', 'codigo', 'descripcion', 'duracion_semestres', 'activa')


class CicloForm(forms.ModelForm):
    class Meta:
        model = Ciclo
        fields = ('carrera', 'numero', 'semestre', 'anio', 'activo')


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ('nombre', 'codigo', 'ciclo', 'creditos', 'horas_teoricas', 'horas_practicas', 'activo')


class HorarioForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = ('curso', 'dia', 'hora_inicio', 'hora_fin', 'aula')
        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time'}),
        }


class AsignacionDocenteForm(forms.ModelForm):
    class Meta:
        model = AsignacionDocente
        fields = ('docente', 'curso')


class InscripcionAlumnoForm(forms.ModelForm):
    class Meta:
        model = InscripcionAlumno
        fields = ('alumno', 'curso', 'ciclo')


class ToleranciaConfigForm(forms.ModelForm):
    class Meta:
        model = ToleranciaConfig
        fields = ('curso', 'docente', 'minutos_tolerancia', 'porcentaje_asistencia_aprobar')
