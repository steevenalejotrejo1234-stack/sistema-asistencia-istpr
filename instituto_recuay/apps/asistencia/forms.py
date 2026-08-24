from django import forms
from .models import RegistroAsistencia, SesionQR, Justificacion


class RegistroAsistenciaForm(forms.ModelForm):
    class Meta:
        model = RegistroAsistencia
        fields = ('alumno', 'curso', 'horario', 'fecha', 'hora_entrada', 'estado', 'observaciones')
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora_entrada': forms.TimeInput(attrs={'type': 'time'}),
        }


class SesionQRForm(forms.ModelForm):
    class Meta:
        model = SesionQR
        fields = ('curso', 'horario')


class JustificacionForm(forms.ModelForm):
    class Meta:
        model = Justificacion
        fields = ('curso', 'fecha_inicial', 'fecha_final', 'motivo', 'archivo_adjunto')
        widgets = {
            'fecha_inicial': forms.DateInput(attrs={'type': 'date'}),
            'fecha_final': forms.DateInput(attrs={'type': 'date'}),
            'motivo': forms.Textarea(attrs={'rows': 4}),
        }


class ResponderJustificacionForm(forms.ModelForm):
    class Meta:
        model = Justificacion
        fields = ('estado', 'respuesta')
        widgets = {
            'respuesta': forms.Textarea(attrs={'rows': 4}),
        }


class EscaneoQRForm(forms.Form):
    token_qr = forms.CharField(max_length=128, widget=forms.HiddenInput())
    codigo_validacion = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el codigo de validacion',
            'autocomplete': 'off'
        })
    )
