(function(angular) {
  'use strict';
angular.module('alineaciones', ['dataService','dialog'])
  
  .component('alineacionesTab', {
    templateUrl: 'static/templates/alineacionesTab.html',
    require: {
       appAdmin: '^appAdmin'
    },
    bindings: { $router: '<' },
    controller: AlineacionesTabComponent
    
  })

  .component('jornadasForm', {
    templateUrl:'static/templates/jornadasForm.html',
    require: {
       appAdmin: '^appAdmin',
       alineacionesTab: '^alineacionesTab'
    },
    bindings: { $router: '<' },
    controller: JornadasFormComponent,
    $canActivate: function($nextInstruction, $prevInstruction) {
      console.log('$canActivate', arguments);
    }
  })

  .component('equiposSelect', {
    templateUrl:'static/templates/equiposSelect.html',
    require: {
       appAdmin: '^appAdmin',
       alineacionesTab: '^alineacionesTab'
    },
    bindings: { $router: '<' },
    controller: EquiposSelectComponent,
    $canActivate: function($nextInstruction, $prevInstruction) {
      console.log('$canActivate', arguments);
    }
  })

  .component('jornadasSelect', {
    templateUrl:'static/templates/jornadasSelect.html',
    require: {
       appAdmin: '^appAdmin',
       alineacionesTab: '^alineacionesTab'
    },
    bindings: { $router: '<' },
    controller: JornadasSelectComponent,
    $canActivate: function($nextInstruction, $prevInstruction) {
      console.log('$canActivate', arguments);
    }
  })

  .component('jugadoresList', {
    templateUrl:'static/templates/jugadoresList.html',
    require: {
       appAdmin: '^appAdmin',
       alineacionesTab: '^alineacionesTab'
    },
    bindings: { $router: '<' },
    controller: JugadoresListComponent,
    $canActivate: function($nextInstruction, $prevInstruction) {
      console.log('$canActivate', arguments);
    }
  })

  .component('alineacionActual', {
    templateUrl:'static/templates/alineacionActual.html',
    require: {
       appAdmin: '^appAdmin',
       alineacionesTab: '^alineacionesTab'
    },
    bindings: { $router: '<' },
    controller: AlineacionActualComponent,
    $canActivate: function($nextInstruction, $prevInstruction) {
      console.log('$canActivate', arguments);
    }
  });


function AlineacionesTabComponent(equiposService,$scope,$filter) {
  var alineacionActual = [];
  var alineacionAnterior = []
  var totalAlineacion = 0;
  var jornadaActual = null;
  var equipoActual = null;
  var filteredList = [];
  var selectedList = [];
  var ctrl = this;

  this.$routerOnActivate = function(next) {
    console.log('$routerOnActivate', this, arguments);
  };

  this.$onInit = function () {
    ctrl.alineacionActual = [];
  }

  $scope.$watch('$ctrl.appAdmin.lista_jornadas',function(newVal,oldVal){
    if (ctrl.appAdmin.lista_jornadas[0]){
       ctrl.jornadaActual = ctrl.appAdmin.lista_jornadas[0].numero;
       ctrl.totalAlineacion = ctrl.getDineroEquipo(ctrl.equipoActual);  
      console.log(ctrl.equipoActual);
      console.log(ctrl.getDineroEquipo(ctrl.equipoActual));   
    }
  });

  $scope.$watch('$ctrl.jornadaActual',function(newVal,oldVal){
    if (ctrl.jornadaActual && ctrl.equipoActual){ctrl.getAlineacionActual();}
  });

  $scope.$watch('$ctrl.equipoActual',function(newVal,oldVal){
    if (ctrl.jornadaActual && ctrl.equipoActual){ctrl.getAlineacionActual();}
  });
  

  this.getAlineacionActual = function(){
    equiposService.getAlineacion(ctrl.jornadaActual,ctrl.equipoActual).then(function(alineacion) {
      ctrl.alineacionActual = alineacion.data;
      if (!ctrl.alineacionActual){
	ctrl.alineacionActual=[];	
      }
      ctrl.selectedList.length = 0;
      ctrl.totalAlineacion = ctrl.getDineroEquipo(ctrl.equipoActual);
      angular.forEach(ctrl.alineacionActual,function(value,index){
          ctrl.selectedList.push(value.id);
          ctrl.totalAlineacion = ctrl.totalAlineacion - value.precio;        
      });        

      //Alineacion anterior
      equiposService.getAlineacion(ctrl.jornadaActual-1,ctrl.equipoActual).then(function(alineacion) {
      ctrl.alineacionAnterior = alineacion.data;
      if (!ctrl.alineacionAnterior ){
	ctrl.alineacionAnterior =[];	
      }
     });  
    });
  }

  this.getDineroEquipo = function(equipo){
     var found = $filter('filter')(ctrl.appAdmin.lista_equipos, {$: equipo}, true);
     return found[0].dinero;	
  }

  this.enviarAlineacion = function(){
     console.log(ctrl.ncambios()) 
     if (ctrl.alineacionActual.length != 11){
        var message = "El equipo debe tener 11 jugadores";
        ctrl.appAdmin.messages = message;
     }else if(ctrl.totalAlineacion<0){
	var message = "No tienes dinero";
        ctrl.appAdmin.messages = message;
     } else if(ctrl.jugadoresPosicion("POR")!=1){
	var message = "El equipo debe tener 1 portero";
        ctrl.appAdmin.messages = message;
     }else if((ctrl.jugadoresPosicion("DEF")<3) || (ctrl.jugadoresPosicion("DEF")>5) ){
	var message = "El equipo debe tener entre 3 y 5 defensas";
        ctrl.appAdmin.messages = message;
     }else if((ctrl.jugadoresPosicion("MED")<3) || (ctrl.jugadoresPosicion("MED")>5) ){
	var message = "El equipo debe tener entre 3 y 5 medios";
        ctrl.appAdmin.messages = message;
     }else if((ctrl.jugadoresPosicion("DEL")<1) || (ctrl.jugadoresPosicion("DEL")>3) ){
	var message = "El equipo debe tener entre 1 y 3 delanteros";
        ctrl.appAdmin.messages = message;
     }else if(ctrl.totalAlineacion<0){
	var message = "No tienes suficiente dinero";
        ctrl.appAdmin.messages = message;
     }else if (ctrl.ncambios()>3){
        var message = "Solo se permiten tres cambios";
        ctrl.appAdmin.messages = message;
     }else{
        ctrl.appAdmin.enviarAlineacion(ctrl.equipoActual,ctrl.jornadaActual,ctrl.alineacionActual);  
     }
  }

  this.jugadoresPosicion = function(posicion){
      var total = 0;
      angular.forEach(ctrl.alineacionActual,function(value,index){
          if (value.posicion == posicion){total = total + 1;}        
      }); 
      return total;
  }

  this.ncambios = function(){
   var diff = ctrl.alineacionAnterior.filter(item => !ctrl.alineacionActual.some(other => item.id === other.id)); 
   return diff.length;
  } 
  
}

function JornadasSelectComponent() {
  var ctrl = this;

  this.$routerOnActivate = function(next) {
    console.log('$routerOnActivate', this, arguments);
  };

  this.$onInit = function () {
    this.alineacionesTab.jornadaActual = null;
    if (this.appAdmin.lista_jornadas[0]){
       this.alineacionesTab.jornadaActual = this.appAdmin.lista_jornadas[0].numero;
    }
    
  };

}

function EquiposSelectComponent() {
  
  var ctrl = this;

  this.$routerOnActivate = function(next) {
    console.log('$routerOnActivate', this, arguments);
  };

  this.$onInit = function () {
    this.alineacionesTab.equipoActual = null;  
    this.alineacionesTab.equipoActual = this.appAdmin.lista_equipos.slice(-1)[0].usuario.username; 
       console.log('Inicializado equipo '+this.alineacionesTab.equipoActual)
  };
   
}

function AlineacionActualComponent($scope) {
  
  var ctrl = this;

  this.$routerOnActivate = function(next) {
    console.log('$routerOnActivate', this, arguments);
  };

 this.$onInit = function () {
    if (ctrl.alineacionesTab.jornadaActual && ctrl.alineacionesTab.equipoActual){ 
       ctrl.alineacionesTab.getAlineacionActual();
    }
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

 this.onRemoveJugador = function(jugador,$index) {
    ctrl.alineacionesTab.alineacionActual.splice(ctrl.alineacionesTab.alineacionActual.indexOf(jugador),1);
    console.log(ctrl.alineacionesTab.alineacionActual);
    ctrl.alineacionesTab.selectedList.splice(ctrl.alineacionesTab.selectedList.indexOf(jugador.id),1);
     ctrl.alineacionesTab.totalAlineacion = ctrl.alineacionesTab.totalAlineacion+jugador.precio;
  }; 

}

function JugadoresListComponent() {
  
  var posicion = "POR";
  var ctrl = this;
  
  this.$routerOnActivate = function(next) {
    console.log('$routerOnActivate', this, arguments);
  };
 
  this.$onInit = function () {
    this.filterJugadores("POR"); 
    ctrl.alineacionesTab.selectedList = [];	
  }; 

  this.isSelected = function(jugador) {
    return (ctrl.alineacionesTab.selectedList.indexOf(jugador.id)!=-1);
  };

  this.onSelectJugador = function(jugador) {
    if (ctrl.alineacionesTab.selectedList.indexOf(jugador.id)==-1){
      ctrl.alineacionesTab.alineacionActual.push(jugador);
      ctrl.alineacionesTab.selectedList.push(jugador.id);
      ctrl.alineacionesTab.totalAlineacion = ctrl.alineacionesTab.totalAlineacion-jugador.precio;
    } else {
      var message = "Jugador ya seleccionado";
      ctrl.appAdmin.messages = message; 
    }
  }; 

  this.onSelectPosicion = function(event) {
    ctrl.posicion = event.target.value;
    ctrl.filterJugadores(ctrl.posicion);
    console.log(ctrl.alineacionesTab.jornadaActual);
  };

  this.filterJugadores = function(posicion) {
        ctrl.filteredList = [];
        angular.forEach(ctrl.appAdmin.lista_jugadores,function(value,index){
                if (value.posicion == posicion){
			ctrl.filteredList.push(value);
			
		}
	})
   console.log(ctrl.filteredList);
  };
}

function JornadasFormComponent() {
  var ctrl = this;
  
  this.create = function(){
   ctrl.appAdmin.createJornada(ctrl.numero,new Date().toJSON());
   //ctrl.appAdmin.createJornada(ctrl.numero,ctrl.limite);
  }
  
}

})(window.angular);

/*
Copyright 2016 Google Inc. All Rights Reserved.
Use of this source code is governed by an MIT-style license that
can be found in the LICENSE file at http://angular.io/license
*/
