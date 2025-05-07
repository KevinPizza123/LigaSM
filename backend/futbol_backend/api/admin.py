from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Arbitro, Club, Equipo, Gol, Jugador, Partido, TarjetaAmarilla, TarjetaRoja, Vocalia


# asignacion usuario y clave para cada equipo 
class EquipoAdminForm(ModelForm):
    class Meta:
        model = Equipo
        fields = '__all__'

class EquipoAdmin(admin.ModelAdmin):
    form = EquipoAdminForm
    list_display = ('nombre_equipo', 'club', 'user')
    # ... otras configuraciones ...

    def save_model(self, request, obj, form, change):
        # Si se está creando un nuevo equipo y no tiene usuario asignado,
        # o si se está modificando y se proporciona un nuevo usuario
        if not obj.user and form.cleaned_data.get('user'):
            pass  # El usuario se asigna directamente en el formulario
        elif obj.user and not form.cleaned_data.get('user'):
            obj.user = None # Desasociar el usuario si se quita en el formulario

        super().save_model(request, obj, form, change)

#jugadores campos admin
class JugadorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'numero', 'equipo', 'amarillas_acumuladas', 'rojas_acumuladas')
    list_filter = ('equipo',)  # Permite filtrar jugadores por equipo
    search_fields = ('nombre', 'numero') # Permite buscar jugadores por nombre o número

#admin de partidos 
class PartidoAdmin(admin.ModelAdmin):
    list_display = ('equipo_local', 'equipo_visitante', 'fecha', 'estado', 'goles_local', 'goles_visitante', 'cambios_local', 'cambios_visitante')
    list_filter = ('estado', 'fecha', 'equipo_local', 'equipo_visitante')
    search_fields = ('equipo_local__nombre_equipo', 'equipo_visitante__nombre_equipo') # Permite buscar por nombre de equipo
    ordering = ('-fecha',) # Ordena los partidos por fecha descendente



#registrar al panel admin django
admin.site.register(Club)
admin.site.register(Equipo, EquipoAdmin)
admin.site.register(Jugador)
admin.site.register(Partido,PartidoAdmin)
admin.site.register(Arbitro)
admin.site.register(Vocalia)
admin.site.register(Gol)
admin.site.register(TarjetaAmarilla)
admin.site.register(TarjetaRoja)