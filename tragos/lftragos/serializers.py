from django.contrib.auth.models import User, Group
from lftragos.models import Equipo, Jornada, Alineacion, Futbolista
from rest_framework import serializers

class JugadorPuntosSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    nombre = serializers.CharField(max_length=30)
    posicion = serializers.CharField(max_length=3)
    club = serializers.CharField(max_length=20)
    precio = serializers.IntegerField()
    puntos = serializers.IntegerField()

class InformeEquiposSerializer(serializers.Serializer):
    equipo = serializers.CharField(max_length=30)
    alineacion = serializers.ListField(child=JugadorPuntosSerializer())

class ClasificacionSerializer(serializers.Serializer):
    usuario = serializers.CharField(max_length=30)
    puntos = serializers.IntegerField()

class ClubSerializer(serializers.Serializer):
    club = serializers.CharField(max_length=20)

class JornadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jornada
        fields = ('id','numero','limite')

class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password')

class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

class EquipoGetSerializer(serializers.ModelSerializer):
    usuario = UserGetSerializer()
    class Meta:
        model = Equipo
        fields = ('id','usuario','dinero', 'puntos_iniciales')
	depth = 1

class EquipoPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipo
        fields = ('usuario','dinero', 'puntos_iniciales')

class AlineacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alineacion
        fields = ('equipo','futbolista', 'jornada')

class FutbolistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Futbolista
        fields = ('id','nombre', 'posicion','club', 'precio')

class FutbolistaPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Futbolista
        fields = ('nombre', 'posicion','club', 'precio')

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
