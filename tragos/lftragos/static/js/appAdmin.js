(function(angular) {
  'use strict';
angular.module('adminApp', ['ngCookies','ngComponentRouter', 'equipos', 'alineaciones', 'puntos', 'clasificaciones', 'dataService'])

.config(function($locationProvider, $httpProvider) {
  $locationProvider.html5Mode(true);
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
})

//.service('equiposService', EquiposService)

.value('$routerRootComponent', 'appAdmin')

.component('appAdmin', {
  templateUrl: 'static/templates/appAdmin.html',
  controller: AppAdminComponent,
  $routeConfig: [
    {path: '/equipos', name: 'Equipos', component: 'equiposTab', useAsDefault: true},
    {path: '/ali', name: 'Alineaciones', component: 'alineacionesTab' },
    {path: '/puntos', name: 'Puntos', component: 'puntosTab' },
    {path: '/clasi', name: 'Clasificaciones', component: 'clasificacionesTab' }
  ]
})

  .component('loginForm', {
    templateUrl:'static/templates/loginForm.html',
    require: {
       appAdmin: '^appAdmin'
    },
    bindings: { $router: '<' },
    controller: LoginFormComponent,
    $canActivate: function($nextInstruction, $prevInstruction) {
      console.log('$canActivate', arguments);
    }
  });


function AppAdminComponent(equiposService,$scope,$cookies,$timeout) {
  var lista_equipos = null;
  var lista_jornadas = null;
  var lista_jugadores = null;
  var lista_clubs = null;
  var clas_equipos = null;
  var messages = null;
  var user_info = null;
  var ctrl = this;

  $scope.$watch('$ctrl.messages',function(newVal,oldVal){
     if (ctrl.messages){
     	$("#myModal").modal()
	$timeout(function () {
	        $("#myModal").modal("hide")
        }, 4000);
     }
  },true);

  ctrl.$onInit = function () {
    equiposService.islogged().then(function(response) {
      if ((response.statusText == "ACCEPTED") || (response.statusText == "Accepted")){
         ctrl.user_info = response.data;
      }
      console.log(ctrl.user_info)
    }, function(response){
         ctrl.user_info = null;
    });
    ctrl.getEquipos();
    ctrl.getJornadas();
    ctrl.getJugadores();
    ctrl.getClubs();
  };

  ctrl.createEquipo = function (username, password, dinero, puntos_iniciales){
    equiposService.createEquipo(username, password, dinero, puntos_iniciales).then(function(response) {
      if ((response.statusText == "CREATED") || (response.statusText == "Created")){
         var message = "Equipo "+ response.data.username+" creado";
      }
      ctrl.messages = message;
      ctrl.getEquipos();
      console.log(response);
   }, function(response){
      ctrl.messages = response;
      console.log(response);
   });
  };

  ctrl.createFutbolista = function (nombre, posicion, club, precio){
    equiposService.postFutbolista(nombre, posicion, club, precio).then(function(response) {
      if ((response.statusText == "CREATED") || (response.statusText == "Created")){
         var message = "Futbolista "+ response.data.nombre+" creado";
      }
      ctrl.messages = message;
      ctrl.getJugadores();
      console.log(response);
   }, function(response){
      ctrl.messages = response;
      console.log(response);
   });
  };

  ctrl.getEquipos = function () {
    equiposService.getEquipos().then(function(equipos) {
      ctrl.lista_equipos = equipos.data;
    });
  };

  ctrl.getClubs = function () {
    equiposService.getClubs().then(function(clubs) {
      ctrl.lista_clubs = clubs.data;
      console.log(ctrl.lista_clubs)
    });
  };

  ctrl.getJornadas = function () {
    equiposService.getJornadas().then(function(jornadas) {
      ctrl.lista_jornadas = jornadas.data;
      ctrl.getClasEquipos();
    });
  };

  ctrl.getJugadores = function () {
    equiposService.getJugadores().then(function(jugadores) {
      ctrl.lista_jugadores = jugadores.data;
    });
  };

  ctrl.getClasEquipos = function(){
    equiposService.getClasificacionTotal(ctrl.lista_jornadas[0].numero).then(function(clasificacion) {
      ctrl.clas_equipos = clasificacion.data;
      if (!ctrl.clas_equipos){
	ctrl.clas_equipos=[];
      }
    });
  }

  ctrl.createJornada = function (numero, limite){
    equiposService.createJornada(numero, limite).then(function(response) {
      if ((response.statusText == "CREATED") || (response.statusText == "Created")){
         var message = "Jornada "+ response.data.numero+" creada";
      }
      ctrl.messages = message;
      ctrl.getJornadas();
      console.log(response);
   }, function(response){
      ctrl.messages = response;
      console.log(response);
   });
  };

  ctrl.enviarAlineacion = function (equipo,jornada,futbolistas){
    equiposService.postAlineacion(equipo,jornada,futbolistas).then(function(response) {
      if ((response.statusText == "CREATED") || (response.statusText == "Created")){
         var message = "Alineacion de "+equipo +" guardada";
      }
      ctrl.messages = message;
      console.log(response);
   }, function(response){
      ctrl.messages = response;
      console.log(response);
   });
  };

  ctrl.enviarPuntos = function(jornada,alineados){
  equiposService.postPuntos(jornada,alineados).then(function(response) {
      if ((response.statusText == "CREATED") || (response.statusText == "Created")){
         var message = "Puntos guardados";
      }
      ctrl.messages = message;
      //ctrl.getEquipos();
      console.log(response);
   }, function(response){
      ctrl.messages = response;
      console.log(response);
   });
  };

  ctrl.userlogin = function(username,password){
  equiposService.postlogin(username,password).then(function(response) {
      if ((response.statusText == "ACCEPTED") || (response.statusText == "Accepted")){
         ctrl.user_info = response.data
         $('#loginModal').modal('hide')
      }
   }, function(response){
      ctrl.messages = response.data['error'];
      console.log(response);
   });
  };
}

function LoginFormComponent() {
  var ctrl = this;

  ctrl.login = function(){
   ctrl.appAdmin.userlogin(ctrl.username,ctrl.password);
  }

}


})(window.angular);
