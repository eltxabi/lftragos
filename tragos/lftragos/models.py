from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Equipo(models.Model):
     usuario = models.OneToOneField(User, on_delete=models.CASCADE)
     dinero = models.IntegerField()
     puntos_iniciales = models.IntegerField(default=0)

     def __unicode__(self):
          return self.usuario.username


class Futbolista(models.Model):
     PORTERO = 'POR'
     DEFENSA = 'DEF'
     MEDIO = 'MED'
     DELANTERO = 'DEL'
     POSICIONES_CHOICES = (
        (PORTERO, 'Portero'),
        (DEFENSA, 'Defensa'),
        (MEDIO, 'Medio'),
        (DELANTERO, 'Delantero'),
     )
     nombre = models.CharField(max_length=30)
     posicion = models.CharField(max_length=3,choices=POSICIONES_CHOICES,)
     club = models.CharField(max_length=20)
     precio = models.IntegerField()

     def __unicode__(self):
          return self.nombre


class Jornada(models.Model):
     numero = models.IntegerField(unique=True)
     limite = models.DateTimeField()

     def __unicode__(self):
          return str(self.numero)
     
     def get_month(self):
          return self.limite.month

     
class Alineacion(models.Model):
     equipo = models.ManyToManyField(Equipo)
     futbolista = models.ManyToManyField(Futbolista)
     jornada = models.ManyToManyField(Jornada)

class Puntuacion(models.Model):
     jornada = models.ManyToManyField(Jornada)
     futbolista = models.ManyToManyField(Futbolista)
     puntos = models.IntegerField(null=True)

