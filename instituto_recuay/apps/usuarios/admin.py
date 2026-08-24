from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('username', 'email', 'first_name', 'last_name', 'dni', 'rol', 'is_active')
    list_filter = ('rol', 'is_active', 'sexo')
    search_fields = ('username', 'email', 'dni', 'first_name', 'last_name')
    ordering = ('-created_at',)
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {
            'fields': ('rol', 'dni', 'telefono', 'sexo', 'fecha_nacimiento', 'direccion', 'foto_perfil', 'codigo_estudiante', 'qr_token')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Adicional', {
            'fields': ('rol', 'dni', 'telefono', 'sexo')
        }),
    )
