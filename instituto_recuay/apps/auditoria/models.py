from django.db import models
from django.conf import settings


class RegistroAuditoria(models.Model):
    class Accion(models.TextChoices):
        CREAR = 'crear', 'Crear'
        EDITAR = 'editar', 'Editar'
        ELIMINAR = 'eliminar', 'Eliminar'
        CONSULTAR = 'consultar', 'Consultar'
        LOGIN = 'login', 'Inicio de Sesion'
        LOGOUT = 'logout', 'Cierre de Sesion'
        EXPORTAR = 'exportar', 'Exportar'
        OTRO = 'otro', 'Otro'

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        related_name='registros_auditoria'
    )
    accion = models.CharField(max_length=20, choices=Accion.choices)
    modelo = models.CharField(max_length=100)
    objeto_id = models.IntegerField(null=True, blank=True)
    descripcion = models.TextField()
    ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Registro de Auditoria'
        verbose_name_plural = 'Registros de Auditoria'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.usuario} - {self.get_accion_display()} - {self.modelo} - {self.created_at}"

    @classmethod
    def registrar(cls, usuario, accion, modelo, descripcion, objeto_id=None, ip=None, user_agent=''):
        return cls.objects.create(
            usuario=usuario, accion=accion, modelo=modelo,
            objeto_id=objeto_id, descripcion=descripcion,
            ip=ip, user_agent=user_agent
        )
