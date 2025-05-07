from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TarjetaAmarilla, TarjetaRoja

@receiver(post_save, sender=TarjetaAmarilla)
def actualizar_amarillas_acumuladas(sender, instance, created, **kwargs):
    if created:
        jugador = instance.jugador
        jugador.amarillas_acumuladas += 1
        jugador.save()

@receiver(post_save, sender=TarjetaRoja)
def actualizar_rojas_acumuladas(sender, instance, created, **kwargs):
    if created:
        jugador = instance.jugador
        jugador.rojas_acumuladas += 1
        jugador.save()