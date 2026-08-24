from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta
from apps.usuarios.models import Usuario


def login_view(request):
    if request.user.is_authenticated:
        return redirigir_por_rol(request.user)

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        from django.contrib.auth import authenticate, login
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)
            try:
                from apps.auditoria.models import RegistroAuditoria
                RegistroAuditoria.registrar(
                    usuario=user, accion='login', modelo='Sesion',
                    descripcion=f'{user.username} inicio sesion',
                    ip=request.META.get('REMOTE_ADDR')
                )
            except Exception:
                pass
            return redirigir_por_rol(user)
        else:
            from django.contrib import messages
            messages.error(request, 'Usuario o contrasena incorrectos.')

    return render(request, 'auth/login.html')


def logout_view(request):
    try:
        from apps.auditoria.models import RegistroAuditoria
        RegistroAuditoria.registrar(
            usuario=request.user, accion='logout', modelo='Sesion',
            descripcion=f'{request.user.username} cerro sesion',
            ip=request.META.get('REMOTE_ADDR')
        )
    except Exception:
        pass
    from django.contrib.auth import logout
    logout(request)
    from django.contrib import messages
    messages.success(request, 'Sesion cerrada exitosamente.')
    return redirect('dashboard:login')


def redirigir_por_rol(usuario):
    rol = usuario.rol
    if rol in ['super_admin', 'admin', 'director']:
        return redirect('dashboard:admin_dashboard')
    elif rol == 'docente':
        return redirect('dashboard:docente_dashboard')
    elif rol == 'alumno':
        return redirect('dashboard:alumno_dashboard')
    return redirect('dashboard:admin_dashboard')


@login_required
def admin_dashboard(request):
    from apps.asistencia.models import RegistroAsistencia
    from apps.academica.models import Carrera, Ciclo, Curso, Horario
    from apps.notificaciones.models import Notificacion

    hoy = timezone.now().date()
    mes_actual = hoy.month
    anio_actual = hoy.year

    total_alumnos = Usuario.objects.filter(rol='alumno', is_active=True).count()
    total_docentes = Usuario.objects.filter(rol='docente', is_active=True).count()
    total_carreras = Carrera.objects.filter(activa=True).count()
    total_cursos = Curso.objects.filter(activo=True).count()
    total_horarios = Horario.objects.filter(activo=True).count()

    asistencias_hoy = RegistroAsistencia.objects.filter(fecha=hoy)
    presentes_hoy = asistencias_hoy.filter(estado='P').count()
    tardanzas_hoy = asistencias_hoy.filter(estado='T').count()
    faltas_hoy = asistencias_hoy.filter(estado='F').count()
    justificados_hoy = asistencias_hoy.filter(estado='J').count()
    total_asistencias_hoy = asistencias_hoy.count()

    dias_mes = []
    presentes_mes = []
    tardanzas_mes = []
    faltas_mes = []
    for dia in range(1, 32):
        try:
            fecha = timezone.datetime(anio_actual, mes_actual, dia).date()
        except ValueError:
            break
        if fecha > hoy:
            break
        dias_mes.append(dia)
        registros_dia = RegistroAsistencia.objects.filter(fecha=fecha)
        presentes_mes.append(registros_dia.filter(estado='P').count())
        tardanzas_mes.append(registros_dia.filter(estado='T').count())
        faltas_mes.append(registros_dia.filter(estado='F').count())

    notificaciones_no_leidas = Notificacion.objects.filter(
        usuario=request.user, leida=False
    ).count()

    registros_recientes = RegistroAsistencia.objects.select_related(
        'alumno', 'curso'
    ).order_by('-created_at')[:10]

    context = {
        'total_alumnos': total_alumnos,
        'total_docentes': total_docentes,
        'total_carreras': total_carreras,
        'total_cursos': total_cursos,
        'total_horarios': total_horarios,
        'presentes_hoy': presentes_hoy,
        'tardanzas_hoy': tardanzas_hoy,
        'faltas_hoy': faltas_hoy,
        'justificados_hoy': justificados_hoy,
        'total_asistencias_hoy': total_asistencias_hoy,
        'dias_mes': dias_mes,
        'presentes_mes': presentes_mes,
        'tardanzas_mes': tardanzas_mes,
        'faltas_mes': faltas_mes,
        'notificaciones_no_leidas': notificaciones_no_leidas,
        'registros_recientes': registros_recientes,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)


@login_required
def docente_dashboard(request):
    from apps.asistencia.models import RegistroAsistencia, SesionQR
    from apps.academica.models import AsignacionDocente
    from apps.notificaciones.models import Notificacion

    hoy = timezone.now().date()
    asignaciones = AsignacionDocente.objects.filter(
        docente=request.user, activa=True
    ).select_related('curso', 'curso__ciclo', 'curso__ciclo__carrera')

    cursos_ids = asignaciones.values_list('curso_id', flat=True)
    asistencias_hoy = RegistroAsistencia.objects.filter(
        curso_id__in=cursos_ids, fecha=hoy
    )
    presentes = asistencias_hoy.filter(estado='P').count()
    tardanzas = asistencias_hoy.filter(estado='T').count()
    faltas = asistencias_hoy.filter(estado='F').count()

    sesiones_activas = SesionQR.objects.filter(
        docente=request.user, activa=True, fecha=hoy
    )

    notificaciones_no_leidas = Notificacion.objects.filter(
        usuario=request.user, leida=False
    ).count()

    registros_recientes = RegistroAsistencia.objects.filter(
        curso_id__in=cursos_ids
    ).select_related('alumno', 'curso').order_by('-created_at')[:10]

    context = {
        'asignaciones': asignaciones,
        'presentes_hoy': presentes,
        'tardanzas_hoy': tardanzas,
        'faltas_hoy': faltas,
        'sesiones_activas': sesiones_activas,
        'notificaciones_no_leidas': notificaciones_no_leidas,
        'registros_recientes': registros_recientes,
    }
    return render(request, 'dashboard/docente_dashboard.html', context)


@login_required
def alumno_dashboard(request):
    from apps.asistencia.models import RegistroAsistencia, Justificacion
    from apps.academica.models import InscripcionAlumno
    from apps.notificaciones.models import Notificacion

    hoy = timezone.now().date()
    inscripciones = InscripcionAlumno.objects.filter(
        alumno=request.user, activa=True
    ).select_related('curso', 'ciclo')

    cursos_ids = inscripciones.values_list('curso_id', flat=True)
    asistencias = RegistroAsistencia.objects.filter(
        alumno=request.user, curso_id__in=cursos_ids
    )

    total_clases = asistencias.count()
    presentes = asistencias.filter(estado='P').count()
    tardanzas = asistencias.filter(estado='T').count()
    faltas = asistencias.filter(estado='F').count()
    justificados = asistencias.filter(estado='J').count()

    porcentaje_asistencia = round((presentes / total_clases * 100) if total_clases > 0 else 0, 1)

    justificaciones_pendientes = Justificacion.objects.filter(
        alumno=request.user, estado='P'
    ).count()

    notificaciones_no_leidas = Notificacion.objects.filter(
        usuario=request.user, leida=False
    ).count()

    asistencias_recientes = asistencias.select_related('curso').order_by('-fecha')[:10]

    context = {
        'inscripciones': inscripciones,
        'total_clases': total_clases,
        'presentes': presentes,
        'tardanzas': tardanzas,
        'faltas': faltas,
        'justificados': justificados,
        'porcentaje_asistencia': porcentaje_asistencia,
        'justificaciones_pendientes': justificaciones_pendientes,
        'notificaciones_no_leidas': notificaciones_no_leidas,
        'asistencias_recientes': asistencias_recientes,
    }
    return render(request, 'dashboard/alumno_dashboard.html', context)


@login_required
def estadisticas_api(request):
    from apps.asistencia.models import RegistroAsistencia

    hoy = timezone.now().date()
    dias = []
    presentes = []
    tardanzas = []
    faltas = []

    for i in range(30):
        fecha = hoy - timedelta(days=29 - i)
        dias.append(fecha.strftime('%d/%m'))
        registros = RegistroAsistencia.objects.filter(fecha=fecha)
        presentes.append(registros.filter(estado='P').count())
        tardanzas.append(registros.filter(estado='T').count())
        faltas.append(registros.filter(estado='F').count())

    return JsonResponse({
        'labels': dias,
        'presentes': presentes,
        'tardanzas': tardanzas,
        'faltas': faltas,
    })
