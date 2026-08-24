from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Usuario
from .forms import UsuarioCreationForm, UsuarioChangeForm, PerfilForm
from apps.auditoria.models import RegistroAuditoria


def redirigir_por_rol(usuario):
    if usuario.rol == 'super_admin' or usuario.rol == 'admin':
        return redirect('dashboard:admin_dashboard')
    elif usuario.rol == 'director':
        return redirect('dashboard:admin_dashboard')
    elif usuario.rol == 'docente':
        return redirect('dashboard:docente_dashboard')
    elif usuario.rol == 'alumno':
        return redirect('dashboard:alumno_dashboard')
    return redirect('dashboard:admin_dashboard')


@login_required
def lista_usuarios(request):
    if request.user.rol not in ['super_admin', 'admin', 'director']:
        messages.error(request, 'No tiene permisos para acceder a esta sección.')
        return redirect('dashboard:admin_dashboard')

    query = request.GET.get('q', '')
    rol_filtro = request.GET.get('rol', '')

    usuarios = Usuario.objects.all()

    if query:
        usuarios = usuarios.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(dni__icontains=query) |
            Q(username__icontains=query) |
            Q(email__icontains=query)
        )

    if rol_filtro:
        usuarios = usuarios.filter(rol=rol_filtro)

    paginator = Paginator(usuarios, 15)
    page = request.GET.get('page')
    usuarios_pagina = paginator.get_page(page)

    context = {
        'usuarios': usuarios_pagina,
        'query': query,
        'rol_filtro': rol_filtro,
        'roles': Usuario.Rol.choices,
        'total_usuarios': Usuario.objects.count(),
    }
    return render(request, 'usuarios/lista_usuarios.html', context)


@login_required
def crear_usuario(request):
    if request.user.rol not in ['super_admin', 'admin', 'director']:
        messages.error(request, 'No tiene permisos para realizar esta acción.')
        return redirect('usuarios:lista_usuarios')

    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST, request.FILES)
        if form.is_valid():
            usuario = form.save()
            RegistroAuditoria.registrar(
                usuario=request.user,
                accion='crear',
                modelo='Usuario',
                objeto_id=usuario.pk,
                descripcion=f'Se creó el usuario {usuario.get_full_name()} ({usuario.dni})',
                ip=request.META.get('REMOTE_ADDR')
            )
            messages.success(request, f'Usuario {usuario.get_full_name()} creado exitosamente.')
            return redirect('usuarios:lista_usuarios')
    else:
        form = UsuarioCreationForm()

    return render(request, 'usuarios/crear_usuario.html', {'form': form})


@login_required
def editar_usuario(request, pk):
    if request.user.rol not in ['super_admin', 'admin', 'director']:
        messages.error(request, 'No tiene permisos para realizar esta acción.')
        return redirect('usuarios:lista_usuarios')

    usuario = get_object_or_404(Usuario, pk=pk)

    if request.method == 'POST':
        form = UsuarioChangeForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            usuario = form.save()
            RegistroAuditoria.registrar(
                usuario=request.user,
                accion='editar',
                modelo='Usuario',
                objeto_id=usuario.pk,
                descripcion=f'Se editó el usuario {usuario.get_full_name()} ({usuario.dni})',
                ip=request.META.get('REMOTE_ADDR')
            )
            messages.success(request, f'Usuario {usuario.get_full_name()} actualizado exitosamente.')
            return redirect('usuarios:lista_usuarios')
    else:
        form = UsuarioChangeForm(instance=usuario)

    return render(request, 'usuarios/editar_usuario.html', {'form': form, 'usuario_obj': usuario})


@login_required
def eliminar_usuario(request, pk):
    if request.user.rol not in ['super_admin', 'admin']:
        messages.error(request, 'No tiene permisos para realizar esta acción.')
        return redirect('usuarios:lista_usuarios')

    usuario = get_object_or_404(Usuario, pk=pk)

    if request.method == 'POST':
        nombre = usuario.get_full_name()
        dni = usuario.dni
        usuario.is_active = False
        usuario.save()
        RegistroAuditoria.registrar(
            usuario=request.user,
            accion='eliminar',
            modelo='Usuario',
            objeto_id=pk,
            descripcion=f'Se desactivó el usuario {nombre} ({dni})',
            ip=request.META.get('REMOTE_ADDR')
        )
        messages.success(request, f'Usuario {nombre} desactivado exitosamente.')
        return redirect('usuarios:lista_usuarios')

    return render(request, 'usuarios/eliminar_usuario.html', {'usuario_obj': usuario})


@login_required
def perfil_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    return render(request, 'usuarios/perfil_usuario.html', {'usuario_obj': usuario})


@login_required
def mi_perfil(request):
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('usuarios:mi_perfil')
    else:
        form = PerfilForm(instance=request.user)

    return render(request, 'usuarios/mi_perfil.html', {'form': form})


@login_required
def cambiar_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Contraseña cambiada exitosamente.')
            return redirect('usuarios:mi_perfil')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'usuarios/cambiar_password.html', {'form': form})
