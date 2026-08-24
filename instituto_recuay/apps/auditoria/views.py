from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import RegistroAuditoria


@login_required
def lista_auditoria(request):
    if request.user.rol not in ['super_admin', 'admin']:
        from django.contrib import messages
        from django.shortcuts import redirect
        messages.error(request, 'No tiene permisos para acceder a la auditoria.')
        return redirect('dashboard:admin_dashboard')

    registros = RegistroAuditoria.objects.select_related('usuario').all()

    accion = request.GET.get('accion')
    modelo = request.GET.get('modelo')
    usuario_id = request.GET.get('usuario')

    if accion:
        registros = registros.filter(accion=accion)
    if modelo:
        registros = registros.filter(modelo__icontains=modelo)
    if usuario_id:
        registros = registros.filter(usuario_id=usuario_id)

    paginator = Paginator(registros, 25)
    page = request.GET.get('page')

    return render(request, 'auditoria/lista_auditoria.html', {
        'registros': paginator.get_page(page),
        'acciones': RegistroAuditoria.Accion.choices,
    })
