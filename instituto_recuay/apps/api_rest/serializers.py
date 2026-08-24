from rest_framework import serializers
from apps.usuarios.models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'dni', 'rol', 'telefono', 'is_active')
        read_only_fields = ('id',)
