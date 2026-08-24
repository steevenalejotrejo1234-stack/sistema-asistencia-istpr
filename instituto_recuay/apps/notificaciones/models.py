from django.db import models
from django.conf import settings


class Notificacion(models.Model):
    class Tipo(models.TextChoices):
        INFO = 'info', 'Informacion'
        AVISO = 'aviso', 'Aviso'
        ALERTA = 'alerta', 'Alerta'
        EXITO = 'exito', 'Exito'

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notificaciones'
    )
    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()
    tipo = models.CharField(max_length=10, choices=Tipo.choices, default=Tipo.INFO)
    leida = models.BooleanField(default=False)
    enlace = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Notificacion'
        verbose_name_plural = 'Notificaciones'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.titulo} - {self.usuario.username}"
