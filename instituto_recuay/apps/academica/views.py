from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Carrera, Ciclo, Curso, Horario, AsignacionDocente, InscripcionAlumno, ToleranciaConfig
from .forms import (
    CarreraForm, CicloForm, CursoForm, HorarioForm,
    AsignacionDocenteForm, InscripcionAlumnoForm, ToleranciaConfigForm
)


def _registrar_auditoria(request, accion, modelo, obj_id, desc):
    try:
        from apps.auditoria.models import RegistroAuditoria
        RegistroAuditoria.registrar(
            usuario=request.user, accion=accion, modelo=modelo,
            objeto_id=obj_id, descripcion=desc, ip=request.META.get('REMOTE_ADDR')
        )
    except Exception:
        pass


@login_required
def lista_carreras(request):
    carreras = Carrera.objects.all()
    paginator = Paginator(carreras, 15)
    page = request.GET.get('page')
    return render(request, 'academica/lista_carreras.html', {'carreras': paginator.get_page(page)})


@login_required
def crear_carrera(request):
    if request.method == 'POST':
        form = CarreraForm(request.POST)
        if form.is_valid():
            obj = form.save()
            _registrar_auditoria(request, 'crear', 'Carrera', obj.pk, f'Se creo la carrera {obj.nombre}')
            messages.success(request, f'Carrera {obj.nombre} creada exitosamente.')
            return redirect('academica:lista_carreras')
    else:
        form = CarreraForm()
    return render(request, 'academica/crear_carrera.html', {'form': form})


@login_required
def editar_carrera(request, pk):
    obj = get_object_or_404(Carrera, pk=pk)
    if request.method == 'POST':
        form = CarreraForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, f'Carrera {obj.nombre} actualizada.')
            return redirect('academica:lista_carreras')
    else:
        form = CarreraForm(instance=obj)
    return render(request, 'academica/editar_carrera.html', {'form': form, 'objeto': obj})


@login_required
def eliminar_carrera(request, pk):
    obj = get_object_or_404(Carrera, pk=pk)
    if request.method == 'POST':
        nombre = obj.nombre
        obj.delete()
        messages.success(request, f'Carrera {nombre} eliminada.')
        return redirect('academica:lista_carreras')
    return render(request, 'academica/eliminar_carrera.html', {'objeto': obj})


@login_required
def lista_ciclos(request):
    ciclos = Ciclo.objects.select_related('carrera').all()
    paginator = Paginator(ciclos, 15)
    page = request.GET.get('page')
    return render(request, 'academica/lista_ciclos.html', {'ciclos': paginator.get_page(page)})


@login_required
def crear_ciclo(request):
    if request.method == 'POST':
        form = CicloForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ciclo creado exitosamente.')
            return redirect('academica:lista_ciclos')
    else:
        form = CicloForm()
    return render(request, 'academica/crear_ciclo.html', {'form': form})


@login_required
def editar_ciclo(request, pk):
    obj = get_object_or_404(Ciclo, pk=pk)
    if request.method == 'POST':
        form = CicloForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ciclo actualizado.')
            return redirect('academica:lista_ciclos')
    else:
        form = CicloForm(instance=obj)
    return render(request, 'academica/editar_ciclo.html', {'form': form, 'objeto': obj})


@login_required
def eliminar_ciclo(request, pk):
    obj = get_object_or_404(Ciclo, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Ciclo eliminado.')
        return redirect('academica:lista_ciclos')
    return render(request, 'academica/eliminar_ciclo.html', {'objeto': obj})


@login_required
def lista_cursos(request):
    cursos = Curso.objects.select_related('ciclo', 'ciclo__carrera').all()
    paginator = Paginator(cursos, 15)
    page = request.GET.get('page')
    return render(request, 'academica/lista_cursos.html', {'cursos': paginator.get_page(page)})


@login_required
def crear_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            obj = form.save()
            messages.success(request, f'Curso {obj.nombre} creado.')
            return redirect('academica:lista_cursos')
    else:
        form = CursoForm()
    return render(request, 'academica/crear_curso.html', {'form': form})


@login_required
def editar_curso(request, pk):
    obj = get_object_or_404(Curso, pk=pk)
    if request.method == 'POST':
        form = CursoForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, f'Curso {obj.nombre} actualizado.')
            return redirect('academica:lista_cursos')
    else:
        form = CursoForm(instance=obj)
    return render(request, 'academica/editar_curso.html', {'form': form, 'objeto': obj})


@login_required
def eliminar_curso(request, pk):
    obj = get_object_or_404(Curso, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Curso eliminado.')
        return redirect('academica:lista_cursos')
    return render(request, 'academica/eliminar_curso.html', {'objeto': obj})


@login_required
def lista_horarios(request):
    horarios = Horario.objects.select_related('curso', 'curso__ciclo', 'curso__ciclo__carrera').all()
    paginator = Paginator(horarios, 15)
    page = request.GET.get('page')
    return render(request, 'academica/lista_horarios.html', {'horarios': paginator.get_page(page)})


@login_required
def crear_horario(request):
    if request.method == 'POST':
        form = HorarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Horario creado exitosamente.')
            return redirect('academica:lista_horarios')
    else:
        form = HorarioForm()
    return render(request, 'academica/crear_horario.html', {'form': form})


@login_required
def editar_horario(request, pk):
    obj = get_object_or_404(Horario, pk=pk)
    if request.method == 'POST':
        form = HorarioForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Horario actualizado.')
            return redirect('academica:lista_horarios')
    else:
        form = HorarioForm(instance=obj)
    return render(request, 'academica/editar_horario.html', {'form': form, 'objeto': obj})


@login_required
def eliminar_horario(request, pk):
    obj = get_object_or_404(Horario, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Horario eliminado.')
        return redirect('academica:lista_horarios')
    return render(request, 'academica/eliminar_horario.html', {'objeto': obj})


@login_required
def lista_asignaciones(request):
    asignaciones = AsignacionDocente.objects.select_related('docente', 'curso').all()
    paginator = Paginator(asignaciones, 15)
    page = request.GET.get('page')
    return render(request, 'academica/lista_asignaciones.html', {'asignaciones': paginator.get_page(page)})


@login_required
def crear_asignacion(request):
    if request.method == 'POST':
        form = AsignacionDocenteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Asignacion creada exitosamente.')
            return redirect('academica:lista_asignaciones')
    else:
        form = AsignacionDocenteForm()
    return render(request, 'academica/crear_asignacion.html', {'form': form})


@login_required
def eliminar_asignacion(request, pk):
    obj = get_object_or_404(AsignacionDocente, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Asignacion eliminada.')
        return redirect('academica:lista_asignaciones')
    return render(request, 'academica/eliminar_asignacion.html', {'objeto': obj})


@login_required
def lista_inscripciones(request):
    inscripciones = InscripcionAlumno.objects.select_related('alumno', 'curso', 'ciclo').all()
    paginator = Paginator(inscripciones, 15)
    page = request.GET.get('page')
    return render(request, 'academica/lista_inscripciones.html', {'inscripciones': paginator.get_page(page)})


@login_required
def crear_inscripcion(request):
    if request.method == 'POST':
        form = InscripcionAlumnoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inscripcion creada exitosamente.')
            return redirect('academica:lista_inscripciones')
    else:
        form = InscripcionAlumnoForm()
    return render(request, 'academica/crear_inscripcion.html', {'form': form})


@login_required
def eliminar_inscripcion(request, pk):
    obj = get_object_or_404(InscripcionAlumno, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Inscripcion eliminada.')
        return redirect('academica:lista_inscripciones')
    return render(request, 'academica/eliminar_inscripcion.html', {'objeto': obj})


@login_required
def lista_tolerancias(request):
    tolerancias = ToleranciaConfig.objects.select_related('curso', 'docente').all()
    paginator = Paginator(tolerancias, 15)
    page = request.GET.get('page')
    return render(request, 'academica/lista_tolerancias.html', {'tolerancias': paginator.get_page(page)})


@login_required
def crear_tolerancia(request):
    if request.method == 'POST':
        form = ToleranciaConfigForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tolerancia configurada exitosamente.')
            return redirect('academica:lista_tolerancias')
    else:
        form = ToleranciaConfigForm()
    return render(request, 'academica/crear_tolerancia.html', {'form': form})


@login_required
def editar_tolerancia(request, pk):
    obj = get_object_or_404(ToleranciaConfig, pk=pk)
    if request.method == 'POST':
        form = ToleranciaConfigForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tolerancia actualizada.')
            return redirect('academica:lista_tolerancias')
    else:
        form = ToleranciaConfigForm(instance=obj)
    return render(request, 'academica/editar_tolerancia.html', {'form': form, 'objeto': obj})
