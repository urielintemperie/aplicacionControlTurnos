from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password


class pacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'

class medicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = '__all__'


class tratamientoForm(forms.ModelForm):
    class Meta:
        model = Tratamiento
        fields = '__all__'


class especialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = ('nombre',)
('estado', 'medico', 'paciente', 'horario', 'tratamiento',)

class obraSocialForm(forms.ModelForm):
    class Meta:
        model = ObraSocial
        fields = ('nombre',)


class turnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = '__all__'
        widgets = {
            'estado': forms.HiddenInput(),
            'estaActivo': forms.HiddenInput(),
            }


class LoginForm(forms.Form):
    username = forms.CharField(label="usuario", max_length=64)
    password = forms.CharField(label="clave", widget=forms.PasswordInput, max_length=64)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        try:
            user = User.objects.get(username=username)
            if not check_password(password, user.password):
                raise forms.ValidationError('Password incorrecto')
        except User.DoesNotExist:
            raise forms.ValidationError("No existe el usuario")
        return user


    def is_valid(self):
        valid = super(LoginForm, self).is_valid()
        if not valid:
            return valid
        return True
