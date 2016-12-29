from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.db.models import Q
import datetime

class pacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'
    def clean_nombre(self):
        print ("clean nombre")
        cd = self.cleaned_data
        nombre = cd.get('nombre')
        if len(nombre) < 3 :
            raise forms.ValidationError("nombre muy corto")
        return nombre

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
#('estado', 'medico', 'paciente', 'horario', 'tratamiento',)

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

class horarioTurnoForm(forms.ModelForm):
    '''
    def __init__(self,*args,**kwargs): 
        #use self to store id
        self.form_medico_id=kwargs.pop("medico_id") 
        super(horarioTurnoForm, self).__init__(*args,**kwargs)
    '''
    class Meta:
        model = HorarioTurno
        fields = ('dia','horaInicio','horaFin',)
    
    def clean (self):
        diaDeLaSemana = ['lunes','martes','miercoles','jueves','viernes','sabado','domingo']
        print('clean funciona')
        '''
        idMedico = self.form_medico_id
        print("id medico")
        print(idMedico)
        print("----------")
        '''
        #print(medicoSeleccionado)
        cd = self.cleaned_data
        print (cd)
        dia = cd['dia']
        print(dia)
        print(dia.weekday())
        print(diaDeLaSemana[dia.weekday()])
        horaInicio = cd['horaInicio']
        print (horaInicio)
        horaFin = cd['horaFin']
        print (horaFin)
        if horaInicio>horaFin :
            raise forms.ValidationError("Franja horaria imposible")
        medico = Medico.objects.get(nombre='Matias')
        #if Turno.objects.filter(horario__dia= dia, estaActivo=True, horario__horaInicio__gte=horaInicio,horario__horaInicio__lte=horaFin).exists() :
        print("horarios trabajo")
        for ht in medico.horario.all():
            print(ht.dia)
            #fecha=datetime.datetime.strptime(dia, "%Y-%m-%d").date()
            print(str(ht.horaInicio))
            print(str(ht.horaFin))
            print("----------")
        #for ht in medico.horario.all():
        coincidenciaConHorarioTrabajo = True
        for ht in medico.horario.all():
            if ht.dia == diaDeLaSemana[dia.weekday()] :
                print("trabaja el dia del turno")
                if ((ht.horaInicio<=horaInicio) and (ht.horaFin>horaFin)) :
                    print("trabaja en el horario del turno")
                    coincidenciaConHorarioTrabajo = False
                    break
        if coincidenciaConHorarioTrabajo :
            raise forms.ValidationError("El medico no trabaja ese dia o a esa hora")
        if Turno.objects.filter(
            Q(horario__dia= dia), Q(estaActivo=True) | 
            Q(horario__horaInicio__gte=horaInicio), Q(horario__horaInicio__lte=horaFin) | 
            Q(horario__horaFin__lte=horaFin), Q(horario__horaFin__gte=horaInicio)
        ).exists() :
            raise forms.ValidationError("el horario esta ocupado")
        return cd
        '''
    def clean_horaFin(self):
        print ("clean horaFin")
        cd = self.cleaned_data
        print(cd)
        horaFin = cd.get('horaFin')
        print (horaFin)

        if True :
            raise forms.ValidationError("funciona el clean horaFin")
        return horaFin
        '''
        '''
    def clean_dia(self):
        print ("clean dia")
        cd = self.cleaned_data
        print(cd)
        horaFin = cd.get('horaFin')
        print (horaFin)

        if True :
            raise forms.ValidationError("funciona el clean dia")
        return horaFin
        '''
        '''
    def clean_horaInicio(self):
        print ("clean horaInicio")
        cd = self.cleaned_data
        #dia = cd.get('dia')
        dia = cd['dia']
        print (dia)
        #horaInicio = cd.get('horaInicio')
        horaInicio = cd['horaInicio']
        print (horaInicio)
        print (cd)
        #horaFin = cd['horaFin']
        #print (horaFin)
        #horaFin = cd.get('horaFin')
        #print (horaFin)
        if Turno.objects.filter(horario__dia= dia, estaActivo=True, horario__horaInicio__gte=horaInicio).exists() :
            raise forms.ValidationError("clean horaInicio funciona")
            '''
        '''
        if Turno.objects.filter(horario__dia= dia, estaActivo=True, horario__horaInicio=horaInicio).exists() :
            raise forms.ValidationError("clean horaInicio funciona")
        '''
        return horaInicio
        '''
    def clean_horaIniio(self):
        print ("clean_horaInicio")
        cd = self.cleaned_data
        hI = cd.get('horaInicio')
        dia = cd.get('dia')
        '''
        '''if Turno.objects.filter(estaActivo = True).exists():
            raise forms.ValidationError("Horario Ocupado")
        return hI
        '''
        '''
        if hI == hI :
            raise forms.VaidationError("el clean funciono")
        return hI
        '''
        
        

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
