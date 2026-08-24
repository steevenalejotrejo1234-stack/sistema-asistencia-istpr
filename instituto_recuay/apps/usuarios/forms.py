from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario


class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'first_name', 'last_name', 'dni', 'rol', 'telefono', 'sexo', 'fecha_nacimiento', 'direccion')
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }


class UsuarioChangeForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'first_name', 'last_name', 'dni', 'rol', 'telefono', 'sexo', 'fecha_nacimiento', 'direccion', 'foto_perfil', 'is_active')
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'email', 'telefono', 'direccion', 'foto_perfil', 'sexo', 'fecha_nacimiento')
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'direccion': forms.Textarea(attrs={'rows': 3}),
        }
