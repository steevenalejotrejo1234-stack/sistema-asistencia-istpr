from django.db import models
from django.conf import settings
from django.utils import timezone


class RegistroAsistencia(models.Model):
    class Estado(models.TextChoices):
        PRESENTE = 'P', 'Presente'
        TARDANZA = 'T', 'Tardanza'
        FALTA = 'F', 'Falta'
        JUSTIFICADO = 'J', 'Justificado'
        PERMISO = 'X', 'Permiso'

    class MetodoRegistro(models.TextChoices):
        QR = 'QR', 'Escaneo QR'
        MANUAL = 'M', 'Manual'
        SISTEMA = 'S', 'Sistema'

    alumno = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='asistencias', limit_choices_to={'rol': 'alumno'}
    )
    curso = models.ForeignKey(
        'academica.Curso', on_delete=models.CASCADE, related_name='asistencias'
    )
    horario = models.ForeignKey(
        'academica.Horario', on_delete=models.SET_NULL, null=True, related_name='asistencias'
    )
    fecha = models.DateField(default=timezone.now)
    hora_entrada = models.TimeField(null=True, blank=True)
    hora_salida = models.TimeField(null=True, blank=True)
    estado = models.CharField(max_length=1, choices=Estado.choices, default=Estado.FALTA)
    metodo_registro = models.CharField(max_length=2, choices=MetodoRegistro.choices, default=MetodoRegistro.MANUAL)
    observaciones = models.TextField(blank=True)
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        related_name='asistencias_registradas'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Registro de Asistencia'
        verbose_name_plural = 'Registros de Asistencia'
        unique_together = ('alumno', 'curso', 'fecha')
        ordering = ['-fecha', '-hora_entrada']

    def __str__(self):
        return f"{self.alumno.get_full_name()} - {self.curso.nombre} - {self.fecha} ({self.get_estado_display()})"

    @property
    def porcentaje_asistencia(self):
        total = RegistroAsistencia.objects.filter(
            alumno=self.alumno, curso=self.curso
        ).exclude(estado='F').count()
        total_clases = RegistroAsistencia.objects.filter(
            curso=self.curso
        ).values('fecha').distinct().count()
        if total_clases == 0:
            return 0
        return round((total / total_clases) * 100, 2)


class SesionQR(models.Model):
    curso = models.ForeignKey(
        'academica.Curso', on_delete=models.CASCADE, related_name='sesiones_qr'
    )
    horario = models.ForeignKey(
        'academica.Horario', on_delete=models.SET_NULL, null=True, related_name='sesiones_qr'
    )
    docente = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='sesiones_qr_creadas', limit_choices_to={'rol': 'docente'}
    )
    token_qr = models.CharField(max_length=64, unique=True)
    fecha = models.DateField(default=timezone.now)
    hora_inicio = models.TimeField(auto_now_add=True)
    hora_fin = models.TimeField(null=True, blank=True)
    activa = models.BooleanField(default=True)
    codigo_validacion = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Sesion QR'
        verbose_name_plural = 'Sesiones QR'
        ordering = ['-created_at']

    def __str__(self):
        return f"QR - {self.curso.nombre} - {self.fecha}"

    def save(self, *args, **kwargs):
        if not self.token_qr:
            import secrets
            self.token_qr = secrets.token_hex(32)
        if not self.codigo_validacion:
            import secrets
            self.codigo_validacion = secrets.token_hex(3).upper()[:6]
        super().save(*args, **kwargs)


class Justificacion(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = 'P', 'Pendiente'
        APROBADA = 'A', 'Aprobada'
        RECHAZADA = 'R', 'Rechazada'

    alumno = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='justificaciones', limit_choices_to={'rol': 'alumno'}
    )
    curso = models.ForeignKey(
        'academica.Curso', on_delete=models.CASCADE, related_name='justificaciones'
    )
    fecha_inicial = models.DateField(verbose_name='Fecha Inicial')
    fecha_final = models.DateField(verbose_name='Fecha Final')
    motivo = models.TextField(verbose_name='Motivo de la Justificacion')
    archivo_adjunto = models.FileField(upload_to='justificaciones/', blank=True, null=True)
    estado = models.CharField(max_length=1, choices=Estado.choices, default=Estado.PENDIENTE)
    respondido_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='justificaciones_respondidas'
    )
    respuesta = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Justificacion'
        verbose_name_plural = 'Justificaciones'
        ordering = ['-created_at']

    def __str__(self):
        return f"Justificacion de {self.alumno.get_full_name()} - {self.get_estado_display()}"
