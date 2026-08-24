from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('docente-panel/', views.docente_dashboard, name='docente_dashboard'),
    path('alumno-panel/', views.alumno_dashboard, name='alumno_dashboard'),
    path('api/estadisticas/', views.estadisticas_api, name='estadisticas_api'),
]
