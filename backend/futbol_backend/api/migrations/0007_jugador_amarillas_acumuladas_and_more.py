# Generated by Django 5.2 on 2025-05-07 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_gol_tarjetaamarilla_tarjetaroja'),
    ]

    operations = [
        migrations.AddField(
            model_name='jugador',
            name='amarillas_acumuladas',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='jugador',
            name='rojas_acumuladas',
            field=models.IntegerField(default=0),
        ),
    ]
