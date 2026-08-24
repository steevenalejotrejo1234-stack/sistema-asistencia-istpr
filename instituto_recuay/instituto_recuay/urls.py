from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda r: redirect('dashboard:login'), name='root'),
    path('', include('apps.dashboard.urls', namespace='dashboard')),
    path('usuarios/', include('apps.usuarios.urls', namespace='usuarios')),
    path('academica/', include('apps.academica.urls', namespace='academica')),
    path('asistencia/', include('apps.asistencia.urls', namespace='asistencia')),
    path('notificaciones/', include('apps.notificaciones.urls', namespace='notificaciones')),
    path('auditoria/', include('apps.auditoria.urls', namespace='auditoria')),
    path('reportes/', include('apps.reportes.urls', namespace='reportes')),
    path('api/', include('apps.api_rest.urls', namespace='api_rest')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = 'Instituto Recuay - Panel de Administración'
admin.site.site_title = 'Instituto Recuay'
admin.site.index_title = 'Gestión del Sistema de Asistencia'
