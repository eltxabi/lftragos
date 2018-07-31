var myModule = angular.module('myModule', []);
myModule.factory('equiposService', function($http) {
var service = {
                response: [],                   
                getEquipos: getEquipos,
		createEquipo: createEquipo
            };
  return service;

  function getEquipos() {
    return $http.get("equipos")
    .success(function(response) {
        service.response = response;
    });
  }

  function createEquipo(username,password,dinero,puntos_iniciales) {
    return $http.post("/equipos/",{username: username, password:  password, dinero: dinero, puntos_iniciales: puntos_iniciales})
    .success(function(response) {
        service.response = response;
    });	
  }
  
});
