from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Notificacion


@login_required
def lista_notificaciones(request):
    notificaciones = Notificacion.objects.filter(usuario=request.user)
    leidas = request.GET.get('leida')
    if leidas is not None:
        notificaciones = notificaciones.filter(leida=leidas == 'true')

    from django.core.paginator import Paginator
    paginator = Paginator(notificaciones, 20)
    page = request.GET.get('page')

    return render(request, 'notificaciones/lista_notificaciones.html', {
        'notificaciones': paginator.get_page(page),
        'no_leidas_count': Notificacion.objects.filter(usuario=request.user, leida=False).count(),
    })


@login_required
def marcar_leida(request, pk):
    notificacion = Notificacion.objects.get(pk=pk, usuario=request.user)
    notificacion.leida = True
    notificacion.save()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    return render(request, 'notificaciones/marcar_leida.html', {'notificacion': notificacion})


@login_required
def marcar_todas_leidas(request):
    Notificacion.objects.filter(usuario=request.user, leida=False).update(leida=True)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    from django.contrib import messages
    messages.success(request, 'Todas las notificaciones marcadas como leidas.')
    return render(request, 'notificaciones/marcar_todas_leidas.html')
