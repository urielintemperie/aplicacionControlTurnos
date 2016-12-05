from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import login, authenticate, logout
from .forms import *
import datetime
from .models import *
from django.db.models import Q

"Pagina Inicio"
def home(request):
    today=str(datetime.date.today())
    return redirect('/cambioDia/'+today)
    #lo redirijo directamente a cambioDia con el dia que es para que ya me cargue los turnos
'''
    if request.method == 'POST':
        form = turnoForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/nuevoTurno')
    else:
        form = turnoForm()

    #form = turnoForm()
    today=datetime.date.today()
    medicos= Medico.objects.all()
    return render(request, 'aplicacionTurnos/home.html', {'today':today.isoformat(), 'medicos':medicos,'form':form})
    #return render(request, 'aplicacionTurnos/home.html', {'today':today.isoformat(), 'medicos':medicos})
'''

def cambioDia(request, dia):

    if request.method == 'POST':
        form = turnoForm(request.POST)
        if form.is_valid():
            turno = form.save(commit=True)
            #return redirect('/nuevoTurno')
            return redirect('/cambioDia/'+str(turno.horario.dia))
    else:
        form = turnoForm()
    turnos = Turno.objects.filter(horario__dia= dia, estaActivo = True)
    medicos= Medico.objects.filter(estaActivo = True)
    return render(request, 'aplicacionTurnos/home.html', {'today':dia, 'turnos':turnos, 'medicos':medicos, 'form':form})
    #return render(request, 'aplicacionTurnos/home.html', {'today':dia})


def changeDay(request, dia, medicopk):
    if request.method == 'POST':
        form = turnoForm(request.POST)
        if form.is_valid():
            turno = form.save(commit=True)
            #return redirect('/nuevoTurno')
            return redirect('/cambioDia/'+str(turno.horario.dia))
    else:
        form = turnoForm()
    turnos = Turno.objects.filter(horario__dia= dia, estaActivo = True, medico__pk=medicopk)
    medicos= Medico.objects.filter(estaActivo = True)
    return render(request, 'aplicacionTurnos/home.html', {'today':dia, 'turnos':turnos, 'medicos':medicos, 'form':form})


'''
def cambioDia(request, dia, medicopk):

    if request.method == 'POST':
        form = turnoForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/nuevoTurno')
    else:
        form = turnoForm()
    turnos = Turno.objects.filter(medico__pk= medicopk, horario__dia= dia, estaActivo = True)
    medicos= Medico.objects.filter(estaActivo = True)
    return render(request, 'aplicacionTurnos/home.html', {'today':dia, 'turnos':turnos, 'medicos':medicos, 'medicoSeleccionado':medicopk, 'form':form})
    #return render(request, 'aplicacionTurnos/home.html', {'today':dia})
'''

"ABM Paciente"
def nuevoPaciente(request):
    pacientes = Paciente.objects.filter(estaActivo = True).order_by('apellido')
    if request.method == 'POST':
        form = pacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save(commit=True)
            paciente.estaActivo = True
            paciente.save()
            return redirect('/nuevoPaciente')
    else:
        form = pacienteForm()
    return render(request, 'aplicacionTurnos/nuevoPaciente.html', {'form': form, 'pacientes':pacientes})


def editarPaciente(request, pk):
    paciente = Paciente.objects.get(pk=pk)
    if request.method == 'POST':
        form = pacienteForm(request.POST, instance = paciente)
        if form.is_valid():
            paciente = form.save(commit=True)
            return redirect('/nuevoPaciente')
    else:
        form = pacienteForm(instance = paciente)
    return render(request, 'aplicacionTurnos/editarPaciente.html',{'form':form})

def eliminarPaciente(request , pk):
    paciente = Paciente.objects.get(pk=pk)
    paciente.estaActivo = False
    paciente.save()
    return redirect ('aplicacionTurnos.views.nuevoPaciente')

"ABM Medico"
def nuevoMedico(request):
    medicos = Medico.objects.filter(estaActivo = True).order_by('apellido')
    if request.method == 'POST':
        form = medicoForm(request.POST)
        if form.is_valid():
            medico = form.save(commit=True)
            medico.estaActivo = True
            medico.save()
            return redirect('/nuevoMedico')
    else:
        form = medicoForm()
    return render(request, 'aplicacionTurnos/nuevoMedico.html',{'form':form, 'medicos':medicos})

def editarMedico(request, pk):
    medico = Medico.objects.get(pk=pk)
    if request.method == 'POST':
        form = medicoForm(request.POST, instance = medico)
        if 'eliminar' in request.POST:
            medico.delete()
            return redirect('/nuevoMedico')
        elif form.is_valid():
            form.save(commit=True)
            return redirect('/nuevoMedico')
    else:
        form = medicoForm(instance = medico)
    return render(request, 'aplicacionTurnos/editarMedico.html',{'form':form})

def eliminarMedico(request , pk):
    medico = Medico.objects.get(pk=pk)
    medico.estaActivo = False
    medico.save()
    return redirect ('aplicacionTurnos.views.nuevoMedico')

"ABM Tratamiento"
def nuevoTratamiento(request):
    tratamientos = Tratamiento.objects.all().order_by('nombre')
    if request.method == 'POST':
        form = tratamientoForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/nuevoTratamiento')
    else:
        form = tratamientoForm()
    return render(request, 'aplicacionTurnos/nuevoTratamiento.html',{'form':form, 'tratamientos':tratamientos})

def editarTratamiento(request, pk):
    tratamiento = Tratamiento.objects.get(pk=pk)
    if request.method == 'POST':
        form = tratamientoForm(request.POST, instance = tratamiento)
        if 'eliminar' in request.POST:
            tratamiento.delete()
            return redirect('/nuevoTratamiento')
        elif form.is_valid():
            form.save(commit=True)
            return redirect('/nuevoTratamiento')
    else:
        form = tratamientoForm(instance = tratamiento)
    return render(request, 'aplicacionTurnos/editarTratamiento.html',{'form':form})

def eliminarTratamiento(request , pk):
    Tratamiento.objects.filter(pk=pk).delete()
    return redirect ('aplicacionTurnos.views.nuevoTratamiento')

"ABM obraSocial"

def nuevoObraSocial(request):
    obrasSociales = ObraSocial.objects.all().order_by('nombre')
    if request.method == 'POST':
        form = obraSocialForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/nuevoObraSocial')
    else:
        form = obraSocialForm()
    return render(request, 'aplicacionTurnos/nuevoObraSocial.html',{'form':form, 'obrasSociales':obrasSociales})

def editarObraSocial(request, pk):
    obraSocial = ObraSocial.objects.get(pk=pk)
    if request.method == 'POST':
        form = obraSocialForm(request.POST, instance = obraSocial)
        if 'eliminar' in request.POST:
            obraSocial.delete()
            return redirect('/editarObraSocial')
        elif form.is_valid():
            form.save(commit=True)
            return redirect('/editarObraSocial')
    else:
        form = obraSocialForm(instance = obraSocial)
    return render(request, 'aplicacionTurnos/editarObraSocial.html',{'form':form})

def eliminarObraSocial(request , pk):
    ObraSocial.objects.filter(pk=pk).delete()
    return redirect ('aplicacionTurnos.views.nuevoObraSocial')

"ABM Especialidad"

def nuevoEspecialidad(request):
    especialidades = Especialidad.objects.all().order_by('nombre')
    if request.method == 'POST':
        form = especialidadForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/nuevoEspecialidad')
    else:
        form = especialidadForm()
    return render(request, 'aplicacionTurnos/nuevoEspecialidad.html',{'form':form, 'especialidades':especialidades})

def editarEspecialidad(request, pk):
    especialidad = Especialidad.objects.get(pk=pk)
    if request.method == 'POST':
        form = especialidadForm(request.POST, instance = especialidad)
        if 'eliminar' in request.POST:
            especialidad.delete()
            return redirect('/editarEspecialidad')
        elif form.is_valid():
            form.save(commit=True)
            return redirect('/editarEspecialidad')
    else:
        form = especialidadForm(instance = especialidad)
    return render(request, 'aplicacionTurnos/editarEspecialidad.html',{'form':form})

def eliminarEspecialidad(request , pk):
    Especialidad.objects.filter(pk=pk).delete()
    return redirect ('aplicacionTurnos.views.nuevoEspecialidad')

"AMB Turno"
def nuevoTurno(request):
    turnos = Turno.objects.filter(estaActivo = True).order_by('horario')
    if request.method == 'POST':
        form = turnoForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/nuevoTurno')
    else:
        form = turnoForm()
    return redirect('/')
    #return render(request, 'aplicacionTurnos/nuevoTurno.html', {'form': form, 'turnos':turnos})


def editarTurno(request, pk):
    turno = Turno.objects.get(pk=pk)
    if request.method == 'POST':
        form = turnoForm(request.POST, instance = turno)
        if 'eliminar' in request.POST:
            turno.delete()
            return redirect('/nuevoTurno')
        elif form.is_valid():
            form.save(commit=True)
            return redirect('/nuevoTurno')
    else:
        form = turnoForm(instance = turno)
    return render(request, 'aplicacionTurnos/editarTurno.html',{'form':form})

def eliminarTurno(request , pk):
    turno = Turno.objects.get(pk=pk)
    diaTurno = str(turno.horario.dia)
    turno.estaActivo = False
    turno.save()
    #return redirect ('/nuevoTurno')
    # redirije al mismo dia desde el que se borro el turno
    return redirect ('/cambioDia/'+diaTurno)

"Login with Model User of django"
class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated():
            return redirect('/')
        else:
            form = LoginForm()
            return render(request, 'aplicacionTurnos/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=User.objects.get(username= request.POST['username']), password=request.POST['password'])
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'aplicacionTurnos/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/login')

def busquedaPaciente(request):
    #pacientes = Paciente.objects.order_by('apellido')
    query = request.GET.get('q','')
    if query:
        qset = (
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(dni__icontains=query)
        )
        #Ademas de los filtros del qset, filtro por si el paciente esta activo o no
        results = Paciente.objects.filter(qset,estaActivo=True).distinct()
    else:
        return redirect('aplicacionTurnos.views.nuevoPaciente')
    if request.method == 'POST':
        form = pacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save(commit=True)
            paciente.estaActivo = True
            paciente.save()
            return redirect('/nuevoPaciente')
    else:
        form = pacienteForm()
    return render(request, 'aplicacionTurnos/nuevoPaciente.html', {'form': form, 'pacientes':results})

def busquedaMedico(request):
    #pacientes = Paciente.objects.order_by('apellido')
    query = request.GET.get('q','')
    if query:
        qset = (
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(dni__icontains=query) |
            Q(especialidad__nombre__icontains=query)
        )
        #Ademas de los filtros del qset, filtro por si el paciente esta activo o no
        results = Medico.objects.filter(qset,estaActivo=True).distinct()
    else:
        return redirect('aplicacionTurnos.views.nuevoMedico')
    if request.method == 'POST':
        form = medicoForm(request.POST)
        if form.is_valid():
            medico = form.save(commit=True)
            medico.estaActivo = True
            medico.save()
            return redirect('/nuevoMedico')
    else:
        form = medicoForm()
    return render(request, 'aplicacionTurnos/nuevoMedico.html',{'form':form, 'medicos':results})

def busquedaEspecialidad(request):
    #pacientes = Paciente.objects.order_by('apellido')
    query = request.GET.get('q','')
    if query:
        qset = (
            Q(nombre__icontains=query)
        )
        #Ademas de los filtros del qset, filtro por si el paciente esta activo o no
        results = Especialidad.objects.filter(qset).distinct()
    else:
        return redirect('aplicacionTurnos.views.nuevoEspecialidad')
    if request.method == 'POST':
        form = especialidadForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('aplicacionTurnos.views.nuevoEspecialidad')
    else:
        form = especialidadForm()
    return render(request, 'aplicacionTurnos/nuevoEspecialidad.html',{'form':form, 'especialidades':results})

def busquedaTratamiento(request):
    #pacientes = Paciente.objects.order_by('apellido')
    query = request.GET.get('q','')
    if query:
        qset = (
            Q(nombre__icontains=query)
        )
        #Ademas de los filtros del qset, filtro por si el paciente esta activo o no
        results = Tratamiento.objects.filter(qset).distinct()
    else:
        return redirect('aplicacionTurnos.views.nuevoTratamiento')
    if request.method == 'POST':
        form = tratamientoForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('aplicacionTurnos.views.nuevoTratamiento')
    else:
        form = tratamientoForm()
    return render(request, 'aplicacionTurnos/nuevoTratamiento.html',{'form':form, 'tratamientos':results})

def busquedaObraSocial(request):
    #pacientes = Paciente.objects.order_by('apellido')
    query = request.GET.get('q','')
    if query:
        qset = (
            Q(nombre__icontains=query)
        )
        #Ademas de los filtros del qset, filtro por si el paciente esta activo o no
        results = ObraSocial.objects.filter(qset).distinct()
    else:
        return redirect('aplicacionTurnos.views.nuevoObraSocial')
    if request.method == 'POST':
        form = obraSocialForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('aplicacionTurnos.views.nuevoObraSocial')
    else:
        form = obraSocialForm()
    return render(request, 'aplicacionTurnos/nuevoObraSocial.html',{'form':form, 'obrasSociales':results})
