from django.contrib import admin
from .models import RegistroAuditoria


@admin.register(RegistroAuditoria)
class RegistroAuditoriaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'accion', 'modelo', 'objeto_id', 'ip', 'created_at')
    list_filter = ('accion', 'modelo', 'created_at')
    search_fields = ('descripcion', 'usuario__username')
    readonly_fields = ('usuario', 'accion', 'modelo', 'objeto_id', 'descripcion', 'ip', 'user_agent', 'created_at')
