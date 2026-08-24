from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from apps.usuarios.models import Usuario
from .serializers import UsuarioSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def api_info(request):
    return Response({
        'nombre': 'ISTPR - Sistema de Asistencia',
        'version': '1.0.0',
        'endpoints': {
            'usuarios': '/api/usuarios/',
            'asistencia': '/api/asistencia/',
            'carreras': '/api/carreras/',
        }
    })
