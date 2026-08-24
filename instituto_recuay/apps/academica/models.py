from django.db import models
from django.conf import settings


class Carrera(models.Model):
    nombre = models.CharField(max_length=200)
    codigo = models.CharField(max_length=20, unique=True)
    descripcion = models.TextField(blank=True)
    duracion_semestres = models.IntegerField(default=6)
    activa = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Carrera'
        verbose_name_plural = 'Carreras'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Ciclo(models.Model):
    class Semestre(models.TextChoices):
        PRIMERO = '1', 'Primer Semestre'
        SEGUNDO = '2', 'Segundo Semestre'

    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, related_name='ciclos')
    numero = models.IntegerField(verbose_name='Numero de Ciclo')
    semestre = models.CharField(max_length=1, choices=Semestre.choices)
    anio = models.IntegerField(verbose_name='Ano Academico')
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Ciclo'
        verbose_name_plural = 'Ciclos'
        unique_together = ('carrera', 'numero', 'semestre', 'anio')
        ordering = ['carrera', 'numero', 'semestre']

    def __str__(self):
        return f"{self.carrera.codigo} - Ciclo {self.numero} ({self.get_semestre_display()} {self.anio})"


class Curso(models.Model):
    nombre = models.CharField(max_length=200)
    codigo = models.CharField(max_length=20, unique=True)
    ciclo = models.ForeignKey(Ciclo, on_delete=models.CASCADE, related_name='cursos')
    creditos = models.IntegerField(default=3)
    horas_teoricas = models.IntegerField(default=4)
    horas_practicas = models.IntegerField(default=2)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['ciclo', 'nombre']

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Horario(models.Model):
    class DiaSemana(models.TextChoices):
        LUNES = 'L', 'Lunes'
        MARTES = 'M', 'Martes'
        MIERCOLES = 'X', 'Miercoles'
        JUEVES = 'J', 'Jueves'
        VIERNES = 'V', 'Viernes'
        SABADO = 'S', 'Sabado'

    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='horarios')
    dia = models.CharField(max_length=1, choices=DiaSemana.choices)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    aula = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Horario'
        verbose_name_plural = 'Horarios'
        unique_together = ('curso', 'dia', 'hora_inicio')
        ordering = ['dia', 'hora_inicio']

    def __str__(self):
        return f"{self.curso.nombre} - {self.get_dia_display()} {self.hora_inicio}-{self.hora_fin}"


class AsignacionDocente(models.Model):
    docente = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='asignaciones_docente',
        limit_choices_to={'rol': 'docente'}
    )
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='asignaciones')
    activa = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Asignacion de Docente'
        verbose_name_plural = 'Asignaciones de Docentes'
        unique_together = ('docente', 'curso')

    def __str__(self):
        return f"{self.docente.get_full_name()} - {self.curso.nombre}"


class InscripcionAlumno(models.Model):
    alumno = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='inscripciones',
        limit_choices_to={'rol': 'alumno'}
    )
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='inscripciones')
    ciclo = models.ForeignKey(Ciclo, on_delete=models.CASCADE, related_name='inscripciones')
    activa = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Inscripcion de Alumno'
        verbose_name_plural = 'Inscripciones de Alumnos'
        unique_together = ('alumno', 'curso', 'ciclo')

    def __str__(self):
        return f"{self.alumno.get_full_name()} - {self.curso.nombre}"


class ToleranciaConfig(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='tolerancias')
    docente = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='tolerancias_config',
        limit_choices_to={'rol': 'docente'}
    )
    minutos_tolerancia = models.IntegerField(default=15, verbose_name='Minutos de Tolerancia')
    porcentaje_asistencia_aprobar = models.DecimalField(
        max_digits=5, decimal_places=2, default=75.00,
        verbose_name='% Asistencia Minima para Aprobar'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Configuracion de Tolerancia'
        verbose_name_plural = 'Configuraciones de Tolerancia'
        unique_together = ('curso', 'docente')

    def __str__(self):
        return f"Tolerancia {self.minutos_tolerancia}min - {self.curso.nombre}"
