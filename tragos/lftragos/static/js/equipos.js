(function(angular) {
  'use strict';
angular.module('equipos', ['dataService','dialog'])

  .component('equiposTab', {
    templateUrl: 'static/templates/equiposTab.html',
    require: {
       appAdmin: '^appAdmin'
    },
    bindings: { $router: '<' },
    controller: EquiposTabComponent,

  })

  .component('equiposList', {
    templateUrl:'static/templates/equiposList.html',
    require: {
       appAdmin: '^appAdmin',
       equiposTab: '^equiposTab'
    },
    bindings: { $router: '<' },
    controller: EquiposListComponent,
    $canActivate: function($nextInstruction, $prevInstruction) {
      console.log('$canActivate', arguments);
    }
  })

  .component('equiposInforme', {
    templateUrl:'static/templates/equiposInforme.html',
    require: {
       appAdmin: '^appAdmin',
       equiposTab: '^equiposTab'
    },
    bindings: { $router: '<' },
    controller: EquiposInformeComponent,
    $canActivate: function($nextInstruction, $prevInstruction) {
      console.log('$canActivate', arguments);
    }
  })

  .component('jugadoresjeList', {
    templateUrl:'static/templates/jugadoresJEList.html',
    require: {
       appAdmin: '^appAdmin',
       equiposTab: '^equiposTab'
    },
    bindings: { $router: '<' },
    controller: JugadoresJEListComponent,
    $canActivate: function($nextInstruction, $prevInstruction) {
      console.log('$canActivate', arguments);
    }
  })

  .component('equiposForm', {
    templateUrl:'static/templates/equiposForm.html',
    require: {
       appAdmin: '^appAdmin',
       equiposTab: '^equiposTab'
    },
    bindings: { $router: '<' },
    controller: EquiposFormComponent,
    $canActivate: function($nextInstruction, $prevInstruction) {
      console.log('$canActivate', arguments);
    }
  })

  .component('futbolistasForm', {
    templateUrl:'static/templates/futbolistasForm.html',
    require: {
       appAdmin: '^appAdmin',
       equiposTab: '^equiposTab'
    },
    bindings: { $router: '<' },
    controller: FutbolistasFormComponent,
    $canActivate: function($nextInstruction, $prevInstruction) {
      console.log('$canActivate', arguments);
    }
  })

  .component('jornadasequipoSelect', {
    templateUrl:'static/templates/jornadasequipoSelect.html',
    require: {
       appAdmin: '^appAdmin',
       equiposTab: '^equiposTab'
    },
    bindings: { $router: '<' },
    controller: JornadasequipoSelectComponent,
    $canActivate: function($nextInstruction, $prevInstruction) {
      console.log('$canActivate', arguments);
    }
  })

function EquiposTabComponent(equiposService,$scope) {
  var ctrl = this;
  var jugadoresJEList = [];
  var jornadaActual = null;
  var equipoActual = null;
  var totalEquipo = 0;
  //var equiposInforme = [];

  this.$routerOnActivate = function(next) {
    console.log('$routerOnActivate', this, arguments);
  };

  $scope.$watch('$ctrl.appAdmin.lista_jornadas',function(newVal,oldVal){
    if (ctrl.appAdmin.lista_jornadas){
       ctrl.jornadaActual = ctrl.appAdmin.lista_jornadas[0].numero;
    }
  });

  $scope.$watch('$ctrl.jornadaActual',function(newVal,oldVal){
    if (ctrl.jornadaActual){ctrl.getPuntosEquipoJornada(ctrl.jornadaActual,ctrl.equipoActual);}
  });

  this.getPuntosEquipoJornada = function(numero,equipo){
    equiposService.getPuntosEquipoJornada(numero,equipo).then(function(jugador) {
      ctrl.jugadoresJEList = jugador.data;
      if (!ctrl.jugadoresJEList){
	ctrl.jugadoresJEList=[];
      }else{
         ctrl.totalEquipo = 0;
         console.log(ctrl.jugadoresJEList)
         for (var i = 0; i < ctrl.jugadoresJEList.length; i++){
            console.log(ctrl.jugadoresJEList[i])
            ctrl.totalEquipo = ctrl.totalEquipo + ctrl.jugadoresJEList[i].puntos;
         }
         console.log("total equipo "+ctrl.totalEquipo)
      }
    });
  }

  this.getInformeEquipos = function(){
    equiposService.getInformeEquipos(ctrl.appAdmin.lista_jornadas[0].numero).then(function(informe) {
      ctrl.equiposInforme = informe.data;
      if (!ctrl.equiposInforme){
	ctrl.equiposInforme=[];
      }
    });
  }

}

function EquiposListComponent($scope) {
  var selectedId = null;
  var ctrl = this;

  this.$routerOnActivate = function(next) {
    console.log('$routerOnActivate', this, arguments);
  };

  $scope.$watch('$ctrl.appAdmin.clas_equipos',function(newVal,oldVal){
     if (ctrl.appAdmin.clas_equipos){
        ctrl.equiposTab.equipoActual = ctrl.appAdmin.clas_equipos[0].usuario
        ctrl.equiposTab.getPuntosEquipoJornada(ctrl.appAdmin.lista_jornadas[0].numero,ctrl.equiposTab.equipoActual );
     }
     console.log("equipo actual:"+ctrl.equiposTab.equipoActual)
  });
 /*
  $scope.$watch('$ctrl.appAdmin.lista_jornadas',function(newVal,oldVal){
     if (ctrl.appAdmin.lista_jornadas){
        ctrl.equiposTab.getInformeEquipos();
     }
  });
*/


  this.onSelect = function(equipo){
   ctrl.equiposTab.equipoActual = equipo.usuario
   ctrl.equiposTab.getPuntosEquipoJornada(ctrl.equiposTab.jornadaActual,equipo.usuario);
  };

  this.isSelected = function(equipo) {
    return (equipo.usuario === ctrl.equiposTab.equipoActual);
  };

}

function JugadoresJEListComponent($scope) {
  var ctrl = this;

  this.$routerOnActivate = function(next) {
    console.log('$routerOnActivate', this, arguments);
  };

  $scope.posicionOrder = function (item) {
        switch (item.posicion) {
            case 'POR':
                return 1;

            case 'DEF':
                return 2;

            case 'MED':
                return 3;

            case 'DEL':
                return 4;
        }
    };

}

function EquiposFormComponent($window) {
  var selectedId = null;
  var ctrl = this;

  this.create = function(){
   ctrl.appAdmin.createEquipo(ctrl.username,ctrl.password,ctrl.dinero,ctrl.puntos_iniciales);
  }

  this.imprimirInforme = function(){
    var url = "http://" + $window.location.host + "/printInforme/"+ctrl.equiposTab.jornadaActual;
    $window.location.href = url;

  }

}

function FutbolistasFormComponent($window) {
  var selectedId = null;
  var ctrl = this;

  this.create = function(){
   ctrl.appAdmin.createFutbolista(ctrl.nombre,ctrl.posicion,ctrl.club,ctrl.precio);
  }
}


function JornadasequipoSelectComponent() {
  var ctrl = this;

  this.$routerOnActivate = function(next) {
    console.log('$routerOnActivate', this, arguments);
  };

  this.$onInit = function () {
    //ctrl.equiposTab.jornadaActual = null;
    if (this.appAdmin.lista_jornadas){
       ctrl.equiposTab.jornadaActual = this.appAdmin.lista_jornadas[0].numero;
    }
    console.log("jorandas actual "+this.equiposTab.jornadaActual )
  };

}


function EquiposInformeComponent() {
  var ctrl = this;


}


})(window.angular);

/*
Copyright 2016 Google Inc. All Rights Reserved.
Use of this source code is governed by an MIT-style license that
can be found in the LICENSE file at http://angular.io/license
*/
