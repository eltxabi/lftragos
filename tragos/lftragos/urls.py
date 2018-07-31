from django.conf.urls import patterns,url
from lftragos import views

urlpatterns = [
   url(r'^$', views.index, name='index'),
   url(r'^login$', views.loginview, name='login'),
   url(r'^logout$', views.logoutpage, name='logout'),
   url(r'^islogged$', views.islogged, name='islogged'),
   url(r'^printInforme/(?P<numero>[0-9]+)/$', views.printInforme, name='printInforme'),
   url(r'^printClasificaciones/(?P<numero>[0-9]+)/$', views.printClasificaciones, name='printClasificaciones'),
   url(r'^printClasificaciones/(?P<numero>[0-9]+)/(?P<numero1>[0-9]+)/(?P<numero2>[0-9]+)/$', views.printClasificaciones, name='printClasificaciones'),
   url(r'^equipos/$', views.equipos, name='equipos'),
   url(r'^clubs/$', views.clubs, name='clubs'),
   url(r'^jornadas/$', views.jornadas, name='jornadas'),
   url(r'^futbolistas/$', views.futbolistas, name='futbolistas'),
   url(r'^alineaciones/$', views.alineaciones, name='alineaciones'),
   url(r'^alineaciones/(?P<numero>[0-9]+)/$', views.alineaciones, name='alineaciones'),
   url(r'^alineaciones/(?P<numero>[0-9]+)/(?P<equipo>\w+)/$', views.alineaciones, name='alineaciones'),
   url(r'^puntos/$', views.puntos, name='puntos'),
   url(r'^puntos/(?P<numero>[0-9]+)/$', views.puntos, name='puntos'),
   url(r'^puntos/(?P<numero>[0-9]+)/(?P<equipo>\w+)/$', views.puntos, name='puntos'),
   url(r'^clasificaciones/total/(?P<numero>[0-9]+)/$', views.clasificaciones_total, name='clasificaciones_total'),
   url(r'^clasificaciones/jornada/(?P<numero>[0-9]+)/$', views.clasificaciones_jornada, name='clasificaciones_jornada'),
   url(r'^clasificaciones/mes/(?P<numero1>[0-9]+)/(?P<numero2>[0-9]+)/$', views.clasificaciones_mes, name='clasificaciones_mes'),
]
