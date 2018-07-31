from django import forms
from django.forms import ModelForm
from lftragos.models import Equipo,Jornada
from django.forms import PasswordInput

class UserForm(forms.Form):
	username = forms.CharField(label='Usuario', max_length=15)
	password = forms.CharField(label='Password', max_length=15, widget=forms.PasswordInput)

class EquipoForm(forms.Form):
    	username = forms.CharField(label='Usuario', max_length=15)
	password = forms.CharField(label='Password', max_length=15, widget=forms.PasswordInput)
	dinero = forms.IntegerField(label='Dinero')
	puntos_iniciales = forms.IntegerField(label='Puntos')

class JornadaForm(ModelForm):
	class Meta:
		model = Jornada
		fields = ['numero', 'limite']
		


	
