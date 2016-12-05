from django.contrib import admin
from .models import HorarioTurno
from .models import HorarioTrabajo
from .models import Medico
from .models import Paciente
from .models import Turno
from .models import ObraSocial
from .models import Tratamiento
from .models import Especialidad

# Register your models here.

admin.site.register(HorarioTurno)
admin.site.register(HorarioTrabajo)
admin.site.register(Medico)
admin.site.register(Paciente)
admin.site.register(Turno)
admin.site.register(ObraSocial)
admin.site.register(Tratamiento)
admin.site.register(Especialidad)

