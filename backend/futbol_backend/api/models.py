from django.db import models
from django.contrib.auth.models import User

#clubs
class Club(models.Model):
    CATEGORIAS_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    nombre_club = models.CharField(max_length=100, unique=True)
    presidente = models.CharField(max_length=100)
    categoria = models.CharField(max_length=1, choices=CATEGORIAS_CHOICES)

    def __str__(self):
        return f"{self.nombre_club} ({self.get_categoria_display()})"

#equipos
class Equipo(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='equipos')
    nombre_equipo = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
   
    def __str__(self):
        return f"{self.nombre_equipo} ({self.club.nombre_club})"    

#jugadores
class Jugador(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='jugadores')
    nombre = models.CharField(max_length=100)
    numero = models.IntegerField()
    amarillas_acumuladas = models.IntegerField(default=0)
    rojas_acumuladas = models.IntegerField(default=0)

    class Meta:
        unique_together = ('equipo', 'numero')

    def __str__(self):
        return f"{self.nombre} (#{self.numero} - {self.equipo.nombre_equipo})"

#partidos
class Partido(models.Model):
    ESTADO_CHOICES = [
        ('P', 'Pendiente'),
        ('J', 'Jugado'),
        ('C', 'Cancelado'),
    ]
    equipo_local = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='partidos_local')
    equipo_visitante = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='partidos_visitante')
    fecha = models.DateTimeField()
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default='P')
    goles_local = models.IntegerField(null=True, blank=True)
    goles_visitante = models.IntegerField(null=True, blank=True)
    cambios_local = models.IntegerField(default=0)
    cambios_visitante = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Partidos'

    def __str__(self):
        return f"{self.equipo_local.nombre_equipo} vs {self.equipo_visitante.nombre_equipo} ({self.fecha.strftime('%d/%m/%Y %H:%M')})"

# arbitros
class Arbitro(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

#vocalias
class Vocalia(models.Model):
    partido = models.OneToOneField(Partido, on_delete=models.CASCADE, related_name='vocalia')
    equipo_vocal = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='vocalias_asignadas')
    arbitro = models.ForeignKey(Arbitro, on_delete=models.SET_NULL, null=True, blank=True)
    jugadores_local_inicial = models.ManyToManyField(Jugador, related_name='vocalia_local_inicial')
    jugadores_visitante_inicial = models.ManyToManyField(Jugador, related_name='vocalia_visitante_inicial')

    def __str__(self):
        return f"Vocalia del partido: {self.partido}"
    
    def calcular_total_vocalia(self):
        total = 12  # Valor fijo

        for jugador in self.jugadores_local_inicial.all():
            total += jugador.amarillas_acumuladas * 0.50
            total += jugador.rojas_acumuladas * 1

        for jugador in self.jugadores_visitante_inicial.all():
            total += jugador.amarillas_acumuladas * 0.50
            total += jugador.rojas_acumuladas * 1

        return round(total, 2)
    
#goles
class Gol(models.Model):
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE, related_name='goles')
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE, related_name='goles_anotados')
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='goles_marcados')
    minuto = models.IntegerField()

    def __str__(self):
        return f"Gol de {self.jugador.nombre} ({self.equipo.nombre_equipo}) al minuto {self.minuto} en el partido {self.partido}"
    
#tarjetas amarillas 
class TarjetaAmarilla(models.Model):
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE, related_name='tarjetas_amarillas')
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE, related_name='amarillas')
    minuto = models.IntegerField()

    def __str__(self):
        return f"Amarilla a {self.jugador.nombre} al minuto {self.minuto} en el partido {self.partido}"
    
#tarjetas rojas
class TarjetaRoja(models.Model):
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE, related_name='tarjetas_rojas')
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE, related_name='rojas')
    minuto = models.IntegerField()

    def __str__(self):
        return f"Roja a {self.jugador.nombre} al minuto {self.minuto} en el partido {self.partido}"
    

