from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.platypus import Spacer, BaseDocTemplate, SimpleDocTemplate, Paragraph, TableStyle,  Frame, FrameBreak, NextPageTemplate, PageBreak, PageTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors,enums
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
from reportlab.lib.pagesizes import A4, inch, landscape
from io import BytesIO

from django.shortcuts import render
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect, HttpResponse
from lftragos.models import Equipo,Jornada,Alineacion,Futbolista,Puntuacion
from lftragos.forms import UserForm,EquipoForm,JornadaForm
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db import connection
from rest_framework import status
from rest_framework.decorators import api_view
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.response import Response
from lftragos.serializers import ClubSerializer, FutbolistaPostSerializer, UserGetSerializer, EquipoGetSerializer,UserPostSerializer, EquipoPostSerializer, JornadaSerializer, FutbolistaSerializer, AlineacionSerializer, JugadorPuntosSerializer, ClasificacionSerializer, InformeEquiposSerializer
import os
from pprint import pprint
# Create your views here.

@api_view(['GET'])
def printClasificaciones(request,numero,numero1=None,numero2=None):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="clasificaciones.pdf"'

    buff = BytesIO()
    doc = BaseDocTemplate(buff,
                            pagesize=A4,
                            rightMargin=5,
                            leftMargin=5,
                            topMargin=5,
                            bottomMargin=5,
                            )


    clasificaciones = []

    styles = getSampleStyleSheet()
    clasificaciones.append(Paragraph("SALDO ANTERIOR__________________________  ",styles['Heading1']))
    clasificaciones.append(Paragraph("RECAUDACION SEMANAL_____________________  ",styles['Heading1']))
    clasificaciones.append(Paragraph("RECAUDACION GENERAL_____________________  ",styles['Heading1']))
    clasificaciones.append(Paragraph("RECAUDACION MENSUAL_____________________  ",styles['Heading1']))
    clasificaciones.append(Paragraph("PAGOS___________________________________  ",styles['Heading1']))
    clasificaciones.append(FrameBreak())
    clasificaciones.append(NextPageTemplate("laterPages"))


    clasificacion_jornada = clas_jornada(numero)
    styles = getSampleStyleSheet()
    clasificaciones.append(Paragraph("Clasificacion Jornada",styles['Heading2']))
    headings = ('Equipo','Puntos')
    clas_jor = [(p.usuario,p.puntos) for p in clasificacion_jornada]
    t = Table([headings] + clas_jor,[doc.width/6,doc.width/20])
    t.setStyle(TableStyle(
         [
            ('ALIGN',(-1,0),(-1,-1),'RIGHT'),
            ('LINEAFTER', (-1, 0), (-1, -1), 1, colors.dodgerblue),
            ('LINEBEFORE', (0, 0), (0, -1), 1, colors.dodgerblue),
            ('BOX', (0, 0), (-1, 0), 2, colors.darkblue)
         ]
    ))

    clasificaciones.append(t)
    clasificaciones.append(Spacer(1,2*inch))

    #clasificaciones.append(FrameBreak())

    clasificacion_total = clas_total(numero)
    styles = getSampleStyleSheet()
    clasificaciones.append(Paragraph("Clasificacion General",styles['Heading2']))
    headings = ('Equipo','Puntos')
    clas_jor = [(p.usuario,p.puntos) for p in clasificacion_total]
    t = Table([headings] + clas_jor,[doc.width/6,doc.width/20])
    t.setStyle(TableStyle(
         [
            ('ALIGN',(-1,0),(-1,-1),'RIGHT'),
            ('LINEAFTER', (-1, 0), (-1, -1), 1, colors.dodgerblue),
            ('LINEBEFORE', (0, 0), (0, -1), 1, colors.dodgerblue),
            ('BOX', (0, 0), (-1, 0), 2, colors.darkblue)
         ]
    ))
    clasificaciones.append(t)
    clasificaciones.append(Spacer(1,2*inch))

    clasificacion_mes = clas_mes(numero1,numero2)
    styles = getSampleStyleSheet()
    clasificaciones.append(Paragraph("Clasificacion Mes",styles['Heading2']))
    headings = ('Equipo','Puntos')
    c_mes = [(p.usuario,p.puntos) for p in clasificacion_mes]
    t = Table([headings] + c_mes,[doc.width/6,doc.width/20])
    t.setStyle(TableStyle(
         [
            ('ALIGN',(-1,0),(-1,-1),'RIGHT'),
            ('LINEAFTER', (-1, 0), (-1, -1), 1, colors.dodgerblue),
            ('LINEBEFORE', (0, 0), (0, -1), 1, colors.dodgerblue),
            ('BOX', (0, 0), (-1, 0), 2, colors.darkblue)
         ]
    ))
    clasificaciones.append(t)

    frameCount = 3
    frameWidth = doc.width/frameCount
    frameHeight = doc.height-0.5*inch
    firstPageHeight = 2.5*inch
    firstPageBottom = frameHeight-firstPageHeight
    framesFirstPage = []
    titleFrame = Frame(doc.leftMargin, firstPageBottom, doc.width, firstPageHeight)
    framesFirstPage.append(titleFrame)




    frames = []
    #construct a frame for each column
    for frame in range(frameCount):

        leftMargin = doc.leftMargin + frame*frameWidth
        column = Frame(leftMargin, doc.bottomMargin, frameWidth, frameHeight)
        frames.append(column)
        firstPageColumn = Frame(leftMargin, doc.bottomMargin, frameWidth, firstPageBottom)
        framesFirstPage.append(firstPageColumn)


    templates = []
    templates.append(PageTemplate(frames=framesFirstPage, id="firstPage"))
    templates.append(PageTemplate(frames=frames, id="laterPages"))
    doc.addPageTemplates(templates)



    #document.build(posts)
    """
    column_gap = 6.5 * cm
    width = doc.width / 4.5

    doc.addPageTemplates(
        [
            PageTemplate(
                frames=[
                    Frame(
                        doc.leftMargin ,
                        doc.bottomMargin,
                        width,
                        doc.height,
                        id='1',
                        rightPadding=0,
                        showBoundary=0  # set to 1 for debugging
                    ),
                    Frame(
                        doc.leftMargin + column_gap ,
                        doc.bottomMargin,
                        width,
                        doc.height,
                        id='2',
                        rightPadding=0,
                        showBoundary=0  # set to 1 for debugging
                    ),
                    Frame(
                        doc.leftMargin + (column_gap*2) ,
                        doc.bottomMargin,
                        width,
                        doc.height,
                        id='3',
                        rightPadding=0,
                        showBoundary=0
                    )
                ]
            ),
        ]
    )
    """
    doc.build(clasificaciones)
    response.write(buff.getvalue())
    buff.close()

    return response

@api_view(['GET'])
def printInforme(request,numero):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="equipoInforme.pdf"'

    buff = BytesIO()
    doc = BaseDocTemplate(buff,
                            pagesize=A4,
                            rightMargin=5,
                            leftMargin=50,
                            topMargin=250,
                            bottomMargin=5,
                            )
    doc.pagesize = landscape(A4)

    equipos = []
    lista_equipos = Equipo.objects.all()
    lista_informe = []
    for equipo in lista_equipos:
        lista_informe.append(InformeEquipo(equipo.usuario.username,puntos_jornada_equipo(numero,equipo.usuario.username)))
    for equipo in lista_informe:
        headings = (equipo.equipo,'')

        dinero_total = 0
        puntos_totales = 0
        for p in equipo.alineacion:
            dinero_total = dinero_total + p.precio
            puntos_totales = puntos_totales + p.puntos
        dinero_equipo = Equipo.objects.filter(usuario__username=equipo.equipo)
        dinero_total = dinero_equipo[0].dinero - dinero_total

        allpuntos = [(p.nombre,p.puntos) for p in equipo.alineacion]
        footer = ('Dinero:'+str(dinero_total),str(puntos_totales))
        t = Table([headings] + allpuntos + [footer],[doc.width/6,doc.width/20])
        t.setStyle(TableStyle(
            [
                ('LINEAFTER', (-1, 0), (-1, -1), 1, colors.dodgerblue),
                ('LINEBEFORE', (0, 0), (0, -1), 1, colors.dodgerblue),
                ('BOX', (0, 0), (-1, 0), 2, colors.darkblue),
                ('BOX', (0, -1), (-1, -1), 2, colors.darkblue)
            ]
        ))
        equipos.append(t)
        equipos.append(Spacer(1,0.7*inch))

    column_gap = 4.5 * cm
    width = doc.width / 4.5
    doc.addPageTemplates(
        [
            PageTemplate(
                frames=[
                    Frame(
                        doc.leftMargin ,
                        doc.bottomMargin,
                        width,
                        doc.height,
                        id='1',
                        rightPadding=0,
                        showBoundary=0  # set to 1 for debugging
                    ),
                    Frame(
                        doc.leftMargin + column_gap ,
                        doc.bottomMargin,
                        width,
                        doc.height,
                        id='2',
                        rightPadding=0,
                        showBoundary=0
                    ),
                     Frame(
                        doc.leftMargin + (column_gap*2) ,
                        doc.bottomMargin,
                        width,
                        doc.height,
                        id='3',
                        rightPadding=0,
                        showBoundary=0  # set to 1 for debugging
                    ),
                    Frame(
                        doc.leftMargin + (column_gap*3),
                        doc.bottomMargin,
                        width,
                        doc.height,
                        id='4',
                        rightPadding=0,
                        showBoundary=0
                    ),
                    Frame(
                        doc.leftMargin + (column_gap*4),
                        doc.bottomMargin,
                        width,
                        doc.height,
                        id='5',
                        rightPadding=0,
                        showBoundary=0  # set to 1 for debugging
                    ),
                    Frame(
                        doc.leftMargin + (column_gap*5),
                        doc.bottomMargin,
                        width,
                        doc.height,
                        id='6',
                        rightPadding=0,
                        showBoundary=0  # set to 1 for debugging
                    ),
                ]
            ),
        ]
    )

    doc.build(equipos)
    response.write(buff.getvalue())
    buff.close()

    return response

@api_view(['GET'])
def islogged(request):
	if request.user.is_authenticated():
		if request.user.is_superuser:
			return Response({'usuario':request.user.id,'username':request.user.username, 'superuser': 'yes'}, status=status.HTTP_202_ACCEPTED)
		else:
			return Response({'usuario':request.user.id,'username':request.user.username, 'superuser': 'no'}, status=status.HTTP_202_ACCEPTED)
	else:
		return Response({'error':'usuario no autenticado'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'POST'])
def loginview(request):
	if request.method == 'POST':
                username = request.data['username']
		password = request.data['password']
		user = authenticate(username=username,password=password)
		if user is not None:
			login(request,user)
                        if user.is_superuser:
				return Response({'usuario':user.id,'username':username, 'superuser': 'yes'}, status=status.HTTP_202_ACCEPTED)
		 	else:
				return Response({'usuario':user.id,'username':username, 'superuser': 'no'}, status=status.HTTP_202_ACCEPTED)
	return Response(
                {'error':'usuario o password incorrectos'}, status=status.HTTP_401_UNAUTHORIZED)


def logoutpage(request):
	logout(request)
        return HttpResponseRedirect("/")

@ensure_csrf_cookie
#@user_passes_test(lambda u: u.is_superuser)
def index(request):
	lista_equipos = Equipo.objects.all()
	lista_jornadas = Jornada.objects.order_by('-numero')
	lista_alineaciones = []
	if len(lista_jornadas)>1:
		lista_alineaciones = Alineacion.objects.filter(jornada__numero=lista_jornadas[0].numero).order_by('equipo__id')
	return render(request,'lftragos/admin.html')

@api_view(['GET'])
def clubs(request):
    if request.method == 'GET':
        lista_clubs = Futbolista.objects.values('club').distinct().order_by('club')
        serializer = ClubSerializer(lista_clubs, many=True)
        return Response(serializer.data)

@api_view(['GET', 'POST'])
def equipos(request):
    if request.method == 'GET':
        lista_equipos = Equipo.objects.all()
        serializer = EquipoGetSerializer(lista_equipos, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if request.user.is_superuser:
		username = request.data['username']
		password = request.data['password']
		dinero = request.data['dinero']
		puntos_iniciales = request.data['puntos_iniciales']
		serializer_user = UserPostSerializer(data={'username':username,'password':password})
		if serializer_user.is_valid():
		    user = serializer_user.save()
		    serializer_equipo = EquipoPostSerializer(data={'usuario':user.id,'dinero':dinero, 'puntos_iniciales':puntos_iniciales})
		    if serializer_equipo.is_valid():
		        serializer_equipo.save()
		        return Response({'usuario':user.id,'username':username,'dinero':dinero, 'puntos_iniciales':puntos_iniciales}, status=status.HTTP_201_CREATED)
		    else:
		        return Response(serializer_equipo.errors, status=status.HTTP_400_BAD_REQUEST)
		else:
		    return Response(
		        serializer_user.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
              return Response({'error':'superuser required'}, status=status.HTTP_401_UNAUTHORIZED)



@api_view(['GET', 'POST'])
def jornadas(request):
    if request.method == 'GET':
        lista_jornadas = Jornada.objects.order_by('-numero')
        serializer = JornadaSerializer(lista_jornadas, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        if request.user.is_superuser:
		serializer = JornadaSerializer(data=request.data)
		if serializer.is_valid():
		    new_jornada = serializer.save()
		    n_jornadas = Jornada.objects.count()
		    if n_jornadas>1:
			lista_alineaciones = Alineacion.objects.filter(jornada__numero=new_jornada.numero-1)
			old_jornada = Jornada.objects.filter(numero=new_jornada.numero-1)
			for alineacion in lista_alineaciones:
		                equipoObject = Equipo.objects.get(pk=alineacion.equipo.all()[0].id)
		                futbolistaObject = Futbolista.objects.get(pk=alineacion.futbolista.all()[0].id)
		                new_ali = Alineacion.objects.create()
		                new_ali.equipo.add(equipoObject)
		                new_ali.futbolista.add(futbolistaObject)
		                new_ali.jornada.add(new_jornada)
				new_ali.save()
		    return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
		    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error':'superuser required'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET','POST'])
def alineaciones(request, numero=None, equipo=None):
    if request.method == 'GET':
        if (equipo!=None):
           lista_jugadores = Futbolista.objects.filter(alineacion__jornada__numero = numero,alineacion__equipo__usuario__username = equipo)
           serializer = FutbolistaSerializer(lista_jugadores, many=True)
        else:
           lista_jugadores = Futbolista.objects.filter(alineacion__jornada__numero = numero).distinct().order_by('club','posicion')
           lista_jugadores_puntos = []
           for jugador in lista_jugadores:
              puntos = Puntuacion.objects.filter(jornada__numero=numero,futbolista__id=jugador.id)
              jugador_puntos_Object = JugadorPuntos(pk=jugador.id,nombre=jugador.nombre,posicion=jugador.posicion,club=jugador.club,precio=jugador.precio)
              if puntos:
                 jugador_puntos_Object.puntos = puntos[0].puntos
              else:
                 jugador_puntos_Object.puntos = 0;
              lista_jugadores_puntos.append(jugador_puntos_Object)
           serializer = JugadorPuntosSerializer(lista_jugadores_puntos, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if request.user.is_superuser:
		equipo = request.data['equipo']
		jornada = request.data['jornada']
		futbolistas = request.data['futbolistas']
		equipoObject = Equipo.objects.filter(usuario__username = equipo)
		jornadaObject = Jornada.objects.filter(numero = jornada)
		futbolistasObject = []
		for futbolista in futbolistas:
		   futbolistasObject.append(Futbolista.objects.get(pk=futbolista['id']))
		if alineacionValida(equipoObject[0],jornadaObject[0],futbolistasObject):
		   Alineacion.objects.filter(equipo=equipoObject[0],jornada=jornadaObject[0]).delete()
		   precio = 0
		   for futbolista in futbolistasObject:
		      alineacion = Alineacion.objects.create()
		      alineacion.jornada.add(jornadaObject[0])
		      alineacion.equipo.add(equipoObject[0])
		      alineacion.futbolista.add(futbolista)
		      alineacion.save()
		      precio = precio + futbolista.precio

		   equipoObject[0].dinero = equipoObject[0].dinero - precio;
		   equipoObject[0].save()
		   return Response({'result' : 'OK'}, status=status.HTTP_201_CREATED)
		else:
		   return Response({'result' : 'Alineacion Invalida'}, status=status.HTTP_400_BAD_REQUEST)
	else:
            return Response({'error':'superuser required'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET','POST'])
def futbolistas(request):
    if request.method == 'GET':
        lista_futbolistas = Futbolista.objects.order_by('club')
        serializer = FutbolistaSerializer(lista_futbolistas, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
       if request.user.is_superuser:
          print(request.data)
          serializer = FutbolistaPostSerializer(data=request.data)
          if serializer.is_valid():
             serializer.save()
             return Response(serializer.data, status=status.HTTP_201_CREATED)
          else:
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       else:
          return Response({'error':'superuser required'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def clasificaciones_jornada(request,numero):
    if request.method == 'GET':
       serializer = ClasificacionSerializer(clas_jornada(numero), many=True)
       return Response(serializer.data)

@api_view(['GET'])
def clasificaciones_total(request,numero):
    if request.method == 'GET':
       serializer = ClasificacionSerializer(clas_total(numero), many=True)
       return Response(serializer.data)

@api_view(['GET'])
def clasificaciones_mes(request,numero1,numero2):
    if request.method == 'GET':
       #jornadaObject = Jornada.objects.filter(numero = numero)
       #list_jornadas = Jornada.objects.filter(limite__month=jornadaObject[0].get_month())
       #mes = jornadaObject[0].get_month()
       #mes1=len(list_jornadas)
       #mes2 =list_jornadas[0].numero
       serializer = ClasificacionSerializer(clas_mes(numero1,numero2), many=True)
       return Response(serializer.data)
       #return Response({'mes' : mes,'mes1':mes1}, status=status.HTTP_201_CREATED)

def alineaciondiff(equipo,jornada,futbolistas):
    lista_jornadas = Jornada.objects.order_by('-numero')
    if len(lista_jornadas)>1:
       lista_jugadores = Futbolista.objects.filter(alineacion__jornada__numero = jornada.numero-1,alineacion__equipo = equipo)
       print(len(set(futbolistas) ^ set(lista_jugadores)))
       return len(set(futbolistas) ^ set(lista_jugadores))
    return True;

def alineacionValida(equipo,jornada,futbolistas):
    portero = 0;
    defensa = 0;
    medio = 0;
    delantero = 0;
    precio = 0;
    for futbolista in futbolistas:
       if (futbolista.posicion=="POR"):
          portero = portero + 1
       elif (futbolista.posicion=="DEF"):
          defensa = defensa + 1
       elif (futbolista.posicion=="MED"):
          medio = medio + 1
       elif (futbolista.posicion=="DEL"):
          delantero = delantero + 1
       precio = precio + futbolista.precio

    return ((len(futbolistas)==11) and (equipo.dinero>=precio) and (portero==1) and (defensa>2) and (defensa<6) and (medio>2) and (medio<6) and (delantero>0) and (delantero<4) and alineaciondiff(equipo,jornada,futbolistas)<=6)

@api_view(['GET', 'POST'])
def puntos(request, numero=None, equipo=None):
   if request.method == 'GET':
      if equipo!=None:
         serializer = JugadorPuntosSerializer(puntos_jornada_equipo(numero,equipo), many=True)
         return Response(serializer.data)
      elif equipo==None:
         lista_equipos = Equipo.objects.all()
         lista_informe = []
         for equipo in lista_equipos:
             lista_informe.append(InformeEquipo(equipo.usuario.username,puntos_jornada_equipo(numero,equipo.usuario.username)))
         serializer = InformeEquiposSerializer(lista_informe,many=True)
         print(serializer)
         return Response(serializer.data)

   elif request.method == 'POST':
      if request.user.is_superuser:
	      jornada = request.data['jornada']
	      futbolistas = request.data['futbolistas']
	      jornadaObject = Jornada.objects.filter(numero = jornada)
	      for futbolista in futbolistas:
		 futbolistaObject = Futbolista.objects.get(pk=futbolista['pk'])
		 puntos = futbolista['puntos']
		 Puntuacion.objects.filter(jornada = jornadaObject[0],futbolista = futbolistaObject).delete()
		 puntuacion = Puntuacion.objects.create()
		 puntuacion.jornada.add(jornadaObject[0])
		 puntuacion.futbolista.add(futbolistaObject)
		 puntuacion.puntos = puntos
		 puntuacion.save()
              os.system('./app-root/repo/mysql-backup')
	      return Response({'result' : 'OK'}, status=status.HTTP_201_CREATED)
      else:
          return Response({'error':'superuser required'}, status=status.HTTP_401_UNAUTHORIZED)


class InformeEquipo(object):
    def __init__(self,equipo,alineacion):
        self.equipo = equipo
        self.alineacion=alineacion

class JugadorPuntos(object):
    def __init__(self, pk, nombre, posicion, club, precio):
        self.pk = pk
        self.nombre = nombre
        self.posicion = posicion
        self.club = club
        self.precio = precio

class Clasificacion(object):
    def __init__(self, usuario, puntos):
        self.usuario = usuario
        self.puntos = puntos

def compare_position(a,b):
    if a.posicion == b.posicion:
       return 0
    elif a.posicion == "POR":
       return -1
    elif b.posicion == "POR":
       return 1
    elif a.posicion == "DEF":
       return -1
    elif b.posicion == "DEF":
       return 1
    elif a.posicion == "MED":
       return -1
    elif a.posicion == "MED":
       return 1
    else:
       return 1


def puntos_jornada_equipo(numero,equipo):
    cursor = connection.cursor()
    cursor.execute(" select lftragos_futbolista.*,puntuacion.puntos from auth_user,lftragos_equipo,lftragos_futbolista,lftragos_jornada,(select futbolista_id,jornada_id,puntos from lftragos_puntuacion,lftragos_puntuacion_jornada,lftragos_puntuacion_futbolista where lftragos_puntuacion_jornada.puntuacion_id=lftragos_puntuacion_futbolista.puntuacion_id and lftragos_puntuacion_futbolista.puntuacion_id=lftragos_puntuacion.id and lftragos_puntuacion_jornada.puntuacion_id=lftragos_puntuacion.id) as puntuacion, (select futbolista_id,jornada_id,equipo_id from lftragos_alineacion,lftragos_alineacion_jornada,lftragos_alineacion_futbolista,lftragos_alineacion_equipo where lftragos_alineacion_jornada.alineacion_id=lftragos_alineacion_futbolista.alineacion_id and lftragos_alineacion_jornada.alineacion_id=lftragos_alineacion_equipo.alineacion_id and lftragos_alineacion_futbolista.alineacion_id=lftragos_alineacion_equipo.alineacion_id  and lftragos_alineacion_futbolista.alineacion_id=lftragos_alineacion.id and lftragos_alineacion_jornada.alineacion_id=lftragos_alineacion.id and lftragos_alineacion_equipo.alineacion_id=lftragos_alineacion.id) as alineacion where (puntuacion.jornada_id = alineacion.jornada_id) and (puntuacion.futbolista_id = alineacion.futbolista_id) and (puntuacion.futbolista_id = lftragos_futbolista.id) and (puntuacion.jornada_id=lftragos_jornada.id) and (lftragos_jornada.numero=%s) and (alineacion.equipo_id=lftragos_equipo.id) and (lftragos_equipo.usuario_id=auth_user.id) and (auth_user.username=%s)",[numero,equipo])

    list_puntos = []
    for row in cursor.fetchall():
       jpuntos = JugadorPuntos(row[0],row[1],row[2],row[3],row[4])
       jpuntos.puntos=row[5]
       list_puntos.append(jpuntos)
    list_puntos.sort(compare_position)
    return list_puntos

def clas_total(numero):
    cursor = connection.cursor()

    cursor.execute("select auth_user.username as usuario, sum(puntuacion.puntos) as puntos from lftragos_equipo,auth_user,(select futbolista_id,jornada_id,puntos from lftragos_puntuacion,lftragos_puntuacion_jornada,lftragos_puntuacion_futbolista where lftragos_puntuacion_jornada.puntuacion_id=lftragos_puntuacion_futbolista.puntuacion_id and lftragos_puntuacion_futbolista.puntuacion_id=lftragos_puntuacion.id and lftragos_puntuacion_jornada.puntuacion_id=lftragos_puntuacion.id) as puntuacion,(select futbolista_id,jornada_id,equipo_id from lftragos_alineacion,lftragos_alineacion_jornada,lftragos_alineacion_futbolista,lftragos_alineacion_equipo where lftragos_alineacion_jornada.alineacion_id=lftragos_alineacion_futbolista.alineacion_id and lftragos_alineacion_jornada.alineacion_id=lftragos_alineacion_equipo.alineacion_id and lftragos_alineacion_futbolista.alineacion_id=lftragos_alineacion_equipo.alineacion_id  and lftragos_alineacion_futbolista.alineacion_id=lftragos_alineacion.id and lftragos_alineacion_jornada.alineacion_id=lftragos_alineacion.id and lftragos_alineacion_equipo.alineacion_id=lftragos_alineacion.id) as alineacion, lftragos_jornada where alineacion.equipo_id=lftragos_equipo.id and lftragos_equipo.usuario_id=auth_user.id and puntuacion.futbolista_id=alineacion.futbolista_id and puntuacion.jornada_id=alineacion.jornada_id and alineacion.jornada_id=lftragos_jornada.id and lftragos_jornada.numero<=%s group by alineacion.equipo_id order by puntos desc",[numero])
    list_clas = []
    for row in cursor.fetchall():
       clas = Clasificacion(row[0],row[1])
       list_clas.append(clas)
    return list_clas

def clas_jornada(numero):
    cursor = connection.cursor()

    cursor.execute("select auth_user.username as usuario, sum(puntuacion.puntos) as puntos from lftragos_equipo,auth_user,(select futbolista_id,jornada_id,puntos from lftragos_puntuacion,lftragos_puntuacion_jornada,lftragos_puntuacion_futbolista where lftragos_puntuacion_jornada.puntuacion_id=lftragos_puntuacion_futbolista.puntuacion_id and lftragos_puntuacion_futbolista.puntuacion_id=lftragos_puntuacion.id and lftragos_puntuacion_jornada.puntuacion_id=lftragos_puntuacion.id) as puntuacion,(select futbolista_id,jornada_id,equipo_id from lftragos_alineacion,lftragos_alineacion_jornada,lftragos_alineacion_futbolista,lftragos_alineacion_equipo where lftragos_alineacion_jornada.alineacion_id=lftragos_alineacion_futbolista.alineacion_id and lftragos_alineacion_jornada.alineacion_id=lftragos_alineacion_equipo.alineacion_id and lftragos_alineacion_futbolista.alineacion_id=lftragos_alineacion_equipo.alineacion_id  and lftragos_alineacion_futbolista.alineacion_id=lftragos_alineacion.id and lftragos_alineacion_jornada.alineacion_id=lftragos_alineacion.id and lftragos_alineacion_equipo.alineacion_id=lftragos_alineacion.id) as alineacion, lftragos_jornada where alineacion.equipo_id=lftragos_equipo.id and lftragos_equipo.usuario_id=auth_user.id and puntuacion.futbolista_id=alineacion.futbolista_id and puntuacion.jornada_id=alineacion.jornada_id and alineacion.jornada_id=lftragos_jornada.id and lftragos_jornada.numero=%s group by alineacion.equipo_id order by puntos desc",[numero])
    list_clas = []
    for row in cursor.fetchall():
       clas = Clasificacion(row[0],row[1])
       list_clas.append(clas)
    return list_clas

def clas_mes(numero1,numero2):
    cursor = connection.cursor()

    cursor.execute("select auth_user.username as usuario, sum(puntuacion.puntos) as puntos from lftragos_equipo,auth_user,(select futbolista_id,jornada_id,puntos from lftragos_puntuacion,lftragos_puntuacion_jornada,lftragos_puntuacion_futbolista where lftragos_puntuacion_jornada.puntuacion_id=lftragos_puntuacion_futbolista.puntuacion_id and lftragos_puntuacion_futbolista.puntuacion_id=lftragos_puntuacion.id and lftragos_puntuacion_jornada.puntuacion_id=lftragos_puntuacion.id) as puntuacion,(select futbolista_id,jornada_id,equipo_id from lftragos_alineacion,lftragos_alineacion_jornada,lftragos_alineacion_futbolista,lftragos_alineacion_equipo where lftragos_alineacion_jornada.alineacion_id=lftragos_alineacion_futbolista.alineacion_id and lftragos_alineacion_jornada.alineacion_id=lftragos_alineacion_equipo.alineacion_id and lftragos_alineacion_futbolista.alineacion_id=lftragos_alineacion_equipo.alineacion_id  and lftragos_alineacion_futbolista.alineacion_id=lftragos_alineacion.id and lftragos_alineacion_jornada.alineacion_id=lftragos_alineacion.id and lftragos_alineacion_equipo.alineacion_id=lftragos_alineacion.id) as alineacion, lftragos_jornada where alineacion.equipo_id=lftragos_equipo.id and lftragos_equipo.usuario_id=auth_user.id and puntuacion.futbolista_id=alineacion.futbolista_id and puntuacion.jornada_id=alineacion.jornada_id and alineacion.jornada_id=lftragos_jornada.id and lftragos_jornada.numero>=%s and lftragos_jornada.numero<=%s group by alineacion.equipo_id order by puntos desc",[numero1,numero2])
    list_clas = []
    for row in cursor.fetchall():
       clas = Clasificacion(row[0],row[1])
       list_clas.append(clas)
    return list_clas
