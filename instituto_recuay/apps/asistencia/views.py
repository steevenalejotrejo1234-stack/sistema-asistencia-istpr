from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
import datetime
from .models import RegistroAsistencia, SesionQR, Justificacion
from .forms import (
    RegistroAsistenciaForm, SesionQRForm, JustificacionForm,
    ResponderJustificacionForm, EscaneoQRForm
)


@login_required
def registrar_asistencia_manual(request):
    if request.user.rol not in ['super_admin', 'admin', 'docente']:
        messages.error(request, 'No tiene permisos para esta accion.')
        return redirect('dashboard:admin_dashboard')

    if request.method == 'POST':
        form = RegistroAsistenciaForm(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.registrado_por = request.user
            registro.metodo_registro = 'M'

            from apps.academica.models import ToleranciaConfig
            try:
                tolerancia = ToleranciaConfig.objects.get(curso=registro.curso, docente=request.user)
                if registro.hora_entrada:
                    horario = registro.horario
                    if horario and registro.hora_entrada > horario.hora_inicio:
                        diff = datetime.datetime.combine(
                            datetime.date.today(), registro.hora_entrada
                        ) - datetime.datetime.combine(
                            datetime.date.today(), horario.hora_inicio
                        )
                        if diff.total_seconds() / 60 > tolerancia.minutos_tolerancia:
                            registro.estado = 'T'
                        else:
                            registro.estado = 'P'
                    else:
                        registro.estado = 'P'
            except ToleranciaConfig.DoesNotExist:
                if registro.hora_entrada and registro.hora_entrada > datetime.time(7, 30):
                    registro.estado = 'T'
                else:
                    registro.estado = 'P'

            registro.save()
            messages.success(request, f'Asistencia registrada para {registro.alumno.get_full_name()}.')
            return redirect('asistencia:historial_asistencias')
    else:
        form = RegistroAsistenciaForm()

    return render(request, 'asistencia/registrar_asistencia.html', {'form': form})


@login_required
def historial_asistencias(request):
    registros = RegistroAsistencia.objects.select_related('alumno', 'curso').all()

    curso_id = request.GET.get('curso')
    fecha = request.GET.get('fecha')
    estado = request.GET.get('estado')
    alumno_search = request.GET.get('alumno', '')

    if curso_id:
        registros = registros.filter(curso_id=curso_id)
    if fecha:
        registros = registros.filter(fecha=fecha)
    if estado:
        registros = registros.filter(estado=estado)
    if alumno_search:
        registros = registros.filter(
            alumno__first_name__icontains=alumno_search
        ) | registros.filter(
            alumno__last_name__icontains=alumno_search
        ) | registros.filter(
            alumno__dni__icontains=alumno_search
        )

    paginator = Paginator(registros, 20)
    page = request.GET.get('page')

    from apps.academica.models import Curso
    context = {
        'registros': paginator.get_page(page),
        'cursos': Curso.objects.filter(activo=True),
        'estados_choices': RegistroAsistencia.Estado.choices,
    }
    return render(request, 'asistencia/historial_asistencias.html', context)


@login_required
def crear_sesion_qr(request):
    if request.user.rol not in ['docente']:
        messages.error(request, 'Solo los docentes pueden crear sesiones QR.')
        return redirect('dashboard:admin_dashboard')

    if request.method == 'POST':
        form = SesionQRForm(request.POST)
        if form.is_valid():
            sesion = form.save(commit=False)
            sesion.docente = request.user
            sesion.save()
            messages.success(request, f'Sesion QR creada. Codigo: {sesion.codigo_validacion}')
            return redirect('asistencia:detalle_sesion_qr', pk=sesion.pk)
    else:
        form = SesionQRForm()

    return render(request, 'asistencia/crear_sesion_qr.html', {'form': form})


@login_required
def detalle_sesion_qr(request, pk):
    sesion = get_object_or_404(SesionQR, pk=pk)
    asistencias = RegistroAsistencia.objects.filter(
        curso=sesion.curso, fecha=sesion.fecha
    ).select_related('alumno')

    return render(request, 'asistencia/detalle_sesion_qr.html', {
        'sesion': sesion,
        'asistencias': asistencias,
    })


@login_required
def escanear_qr(request):
    if request.method == 'POST':
        token_qr = request.POST.get('token_qr', '')
        codigo = request.POST.get('codigo_validacion', '')

        try:
            sesion = SesionQR.objects.get(token_qr=token_qr, activa=True)
        except SesionQR.DoesNotExist:
            messages.error(request, 'Sesion QR no valida o expirada.')
            return render(request, 'asistencia/escanear_qr.html')

        if sesion.codigo_validacion != codigo.upper():
            messages.error(request, 'Codigo de validacion incorrecto.')
            return render(request, 'asistencia/escanear_qr.html', {'sesion': sesion, 'token_qr': token_qr})

        if RegistroAsistencia.objects.filter(
            alumno=request.user, curso=sesion.curso, fecha=timezone.now().date()
        ).exists():
            messages.warning(request, 'Ya registro asistencia para esta sesion.')
            return redirect('asistencia:historial_asistencias')

        registro = RegistroAsistencia(
            alumno=request.user,
            curso=sesion.curso,
            horario=sesion.horario,
            fecha=timezone.now().date(),
            hora_entrada=timezone.now().time(),
            estado='P',
            metodo_registro='QR',
            registrado_por=sesion.docente,
        )
        registro.save()
        messages.success(request, f'Asistencia registrada exitosamente para {sesion.curso.nombre}.')
        return redirect('asistencia:historial_asistencias')

    return render(request, 'asistencia/escanear_qr.html')


@login_required
def escanear_qr_camara(request):
    return render(request, 'asistencia/escanear_qr_camara.html')


@login_required
def validar_qr_ajax(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token_qr = data.get('token_qr', '')
            codigo = data.get('codigo_validacion', '')

            sesion = SesionQR.objects.get(token_qr=token_qr, activa=True)

            if sesion.codigo_validacion != codigo.upper():
                return JsonResponse({'success': False, 'message': 'Codigo incorrecto.'})

            if RegistroAsistencia.objects.filter(
                alumno=request.user, curso=sesion.curso, fecha=timezone.now().date()
            ).exists():
                return JsonResponse({'success': False, 'message': 'Ya registro asistencia.'})

            RegistroAsistencia.objects.create(
                alumno=request.user,
                curso=sesion.curso,
                horario=sesion.horario,
                fecha=timezone.now().date(),
                hora_entrada=timezone.now().time(),
                estado='P',
                metodo_registro='QR',
                registrado_por=sesion.docente,
            )
            return JsonResponse({'success': True, 'message': f'Asistencia registrada para {sesion.curso.nombre}.'})
        except SesionQR.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Sesion QR no valida.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Metodo no permitido.'})


@login_required
def lista_justificaciones(request):
    justificaciones = Justificacion.objects.select_related('alumno', 'curso').all()

    if request.user.rol == 'alumno':
        justificaciones = justificaciones.filter(alumno=request.user)
    elif request.user.rol == 'docente':
        from apps.academica.models import AsignacionDocente
        cursos_ids = AsignacionDocente.objects.filter(
            docente=request.user, activa=True
        ).values_list('curso_id', flat=True)
        justificaciones = justificaciones.filter(curso_id__in=cursos_ids)

    estado = request.GET.get('estado')
    if estado:
        justificaciones = justificaciones.filter(estado=estado)

    paginator = Paginator(justificaciones, 15)
    page = request.GET.get('page')

    return render(request, 'asistencia/lista_justificaciones.html', {
        'justificaciones': paginator.get_page(page),
        'estados_choices': Justificacion.Estado.choices,
    })


@login_required
def crear_justificacion(request):
    if request.method == 'POST':
        form = JustificacionForm(request.POST, request.FILES)
        if form.is_valid():
            justificacion = form.save(commit=False)
            justificacion.alumno = request.user
            justificacion.save()
            messages.success(request, 'Justificacion enviada exitosamente.')
            return redirect('asistencia:lista_justificaciones')
    else:
        form = JustificacionForm()
    return render(request, 'asistencia/crear_justificacion.html', {'form': form})


@login_required
def responder_justificacion(request, pk):
    if request.user.rol not in ['super_admin', 'admin', 'docente']:
        messages.error(request, 'No tiene permisos para esta accion.')
        return redirect('asistencia:lista_justificaciones')

    justificacion = get_object_or_404(Justificacion, pk=pk)

    if request.method == 'POST':
        form = ResponderJustificacionForm(request.POST, instance=justificacion)
        if form.is_valid():
            justificacion = form.save(commit=False)
            justificacion.respondido_por = request.user
            justificacion.save()

            from apps.notificaciones.models import Notificacion
            Notificacion.objects.create(
                usuario=justificacion.alumno,
                titulo='Justificacion Respondida',
                mensaje=f'Su justificacion para {justificacion.curso.nombre} fue {justificacion.get_estado_display()}.',
                tipo='info'
            )
            messages.success(request, 'Justificacion respondida.')
            return redirect('asistencia:lista_justificaciones')
    else:
        form = ResponderJustificacionForm(instance=justificacion)

    return render(request, 'asistencia/responder_justificacion.html', {
        'form': form, 'justificacion': justificacion
    })


@login_required
def mis_asistencias(request):
    registros = RegistroAsistencia.objects.filter(alumno=request.user).select_related('curso')

    curso_id = request.GET.get('curso')
    if curso_id:
        registros = registros.filter(curso_id=curso_id)

    from apps.academica.models import InscripcionAlumno
    cursos_inscritos = InscripcionAlumno.objects.filter(
        alumno=request.user, activa=True
    ).select_related('curso')

    paginator = Paginator(registros, 20)
    page = request.GET.get('page')

    return render(request, 'asistencia/mis_asistencias.html', {
        'registros': paginator.get_page(page),
        'cursos_inscritos': cursos_inscritos,
    })


@login_required
@require_POST
def cerrar_sesion_qr(request, pk):
    if request.user.rol not in ['docente', 'super_admin', 'admin']:
        return JsonResponse({'success': False, 'message': 'Sin permisos.'})

    sesion = get_object_or_404(SesionQR, pk=pk, docente=request.user)
    sesion.activa = False
    sesion.hora_fin = timezone.now().time()
    sesion.save()

    return JsonResponse({'success': True, 'message': 'Sesion QR cerrada.'})
