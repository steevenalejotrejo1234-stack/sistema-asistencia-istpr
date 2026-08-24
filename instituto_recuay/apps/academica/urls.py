from django.urls import path
from . import views

app_name = 'academica'

urlpatterns = [
    path('carreras/', views.lista_carreras, name='lista_carreras'),
    path('carreras/crear/', views.crear_carrera, name='crear_carrera'),
    path('carreras/<int:pk>/editar/', views.editar_carrera, name='editar_carrera'),
    path('carreras/<int:pk>/eliminar/', views.eliminar_carrera, name='eliminar_carrera'),

    path('ciclos/', views.lista_ciclos, name='lista_ciclos'),
    path('ciclos/crear/', views.crear_ciclo, name='crear_ciclo'),
    path('ciclos/<int:pk>/editar/', views.editar_ciclo, name='editar_ciclo'),
    path('ciclos/<int:pk>/eliminar/', views.eliminar_ciclo, name='eliminar_ciclo'),

    path('cursos/', views.lista_cursos, name='lista_cursos'),
    path('cursos/crear/', views.crear_curso, name='crear_curso'),
    path('cursos/<int:pk>/editar/', views.editar_curso, name='editar_curso'),
    path('cursos/<int:pk>/eliminar/', views.eliminar_curso, name='eliminar_curso'),

    path('horarios/', views.lista_horarios, name='lista_horarios'),
    path('horarios/crear/', views.crear_horario, name='crear_horario'),
    path('horarios/<int:pk>/editar/', views.editar_horario, name='editar_horario'),
    path('horarios/<int:pk>/eliminar/', views.eliminar_horario, name='eliminar_horario'),

    path('asignaciones/', views.lista_asignaciones, name='lista_asignaciones'),
    path('asignaciones/crear/', views.crear_asignacion, name='crear_asignacion'),
    path('asignaciones/<int:pk>/eliminar/', views.eliminar_asignacion, name='eliminar_asignacion'),

    path('inscripciones/', views.lista_inscripciones, name='lista_inscripciones'),
    path('inscripciones/crear/', views.crear_inscripcion, name='crear_inscripcion'),
    path('inscripciones/<int:pk>/eliminar/', views.eliminar_inscripcion, name='eliminar_inscripcion'),

    path('tolerancias/', views.lista_tolerancias, name='lista_tolerancias'),
    path('tolerancias/crear/', views.crear_tolerancia, name='crear_tolerancia'),
    path('tolerancias/<int:pk>/editar/', views.editar_tolerancia, name='editar_tolerancia'),
]
