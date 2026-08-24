from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from .managers import UsuarioManager


class Usuario(AbstractUser):
    class Rol(models.TextChoices):
        SUPER_ADMIN = 'super_admin', 'Super Administrador'
        ADMIN = 'admin', 'Administrador'
        DIRECTOR = 'director', 'Director'
        DOCENTE = 'docente', 'Docente'
        ALUMNO = 'alumno', 'Alumno'

    class Sexo(models.TextChoices):
        MASCULINO = 'M', 'Masculino'
        FEMENINO = 'F', 'Femenino'

    telefono_regex = RegexValidator(regex=r'^\+?[\d\s-]{9,15}$')

    rol = models.CharField(max_length=20, choices=Rol.choices, default=Rol.ALUMNO)
    dni = models.CharField(max_length=8, unique=True, verbose_name='DNI')
    telefono = models.CharField(max_length=15, blank=True, validators=[telefono_regex])
    sexo = models.CharField(max_length=1, choices=Sexo.choices, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    direccion = models.TextField(blank=True)
    foto_perfil = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    codigo_estudiante = models.CharField(max_length=20, blank=True, unique=True, null=True)
    qr_token = models.CharField(max_length=64, blank=True, unique=True, null=True)
    qr_foto = models.ImageField(upload_to='certificados_qr/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UsuarioManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_full_name()} ({self.dni})"

    def save(self, *args, **kwargs):
        import secrets
        if not self.qr_token:
            self.qr_token = secrets.token_hex(32)
        if not self.codigo_estudiante and self.rol == self.Rol.ALUMNO:
            self.codigo_estudiante = f"ALU-{self.dni}"
        elif not self.codigo_estudiante and self.rol == self.Rol.DOCENTE:
            self.codigo_estudiante = f"DOC-{self.dni}"
        super().save(*args, **kwargs)

    @property
    def tiene_foto_perfil(self):
        return bool(self.foto_perfil)

    @property
    def iniciales(self):
        nombres = self.first_name.split() if self.first_name else ['?']
        apellidos = self.last_name.split() if self.last_name else ['?']
        return f"{nombres[0][0] if nombres else '?'}{apellidos[0][0] if apellidos else '?'}".upper()
