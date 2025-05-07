from django.db.models import Count
from .models import Gol
from .models import Equipo, Partido

#funciones de calculo 
#tabla posiciones
def calcular_tabla_posiciones():
    tabla = {}
    equipos = Equipo.objects.all()

    for equipo in equipos:
        partidos_local = Partido.objects.filter(equipo_local=equipo, estado='J')
        partidos_visitante = Partido.objects.filter(equipo_visitante=equipo, estado='J')

        partidos_jugados = partidos_local.count() + partidos_visitante.count()
        partidos_ganados = 0
        partidos_empatados = 0
        partidos_perdidos = 0
        goles_favor = 0
        goles_contra = 0
        puntos = 0

        for partido in partidos_local:
            if partido.goles_local is not None and partido.goles_visitante is not None:
                goles_favor += partido.goles_local
                goles_contra += partido.goles_visitante
                if partido.goles_local > partido.goles_visitante:
                    partidos_ganados += 1
                    puntos += 3
                elif partido.goles_local == partido.goles_visitante:
                    partidos_empatados += 1
                    puntos += 1
                else:
                    partidos_perdidos += 1

        for partido in partidos_visitante:
            if partido.goles_local is not None and partido.goles_visitante is not None:
                goles_favor += partido.goles_visitante
                goles_contra += partido.goles_local
                if partido.goles_visitante > partido.goles_local:
                    partidos_ganados += 1
                    puntos += 3
                elif partido.goles_visitante == partido.goles_local:
                    partidos_empatados += 1
                    puntos += 1
                else:
                    partidos_perdidos += 1

        tabla[equipo.id] = {
            'nombre_equipo': equipo.nombre_equipo,
            'club': equipo.club.nombre_club,
            'pj': partidos_jugados,
            'pg': partidos_ganados,
            'pe': partidos_empatados,
            'pp': partidos_perdidos,
            'gf': goles_favor,
            'gc': goles_contra,
            'dif': goles_favor - goles_contra,
            'pts': puntos,
        }

    # Ordenar la tabla por puntos (descendente) y luego por diferencia de goles (descendente)
    tabla_ordenada = sorted(tabla.values(), key=lambda x: (x['pts'], x['dif']), reverse=True)
    return tabla_ordenada

#tabla goleadores   
def calcular_tabla_goleadores():
    goleadores = Gol.objects.values('jugador__nombre', 'jugador__equipo__nombre_equipo', 'jugador__equipo__club__nombre_club').annotate(total_goles=Count('jugador')).order_by('-total_goles')
    return list(goleadores)