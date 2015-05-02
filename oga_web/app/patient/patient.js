'use strict';
angular.module('oga_web.patient', ["ngRoute", "ngMaterial", "ngMdIcons", "ui.bootstrap", "oga_web.patients"])
.config(['$routeProvider', function($routeProvider) {
	$routeProvider.when("/patient_new", {
		templateUrl: "patient/patient.html",
		controller: "patientNewCtrl",
	})
}])
.controller('patientNewCtrl', function($scope, ogaFacade, $location){
	$scope.open = function($event) {
		$event.preventDefault();
		$event.stopPropagation();
		$scope.opened = true;
	};
	$scope.save = function(){
		ogaFacade.addPatient($scope.patient).success(function (data, status, headers, config) {
			$location.path('/patients');
		})
		.error(function(data, status, headers, config){
			alert('Error: '+status + ' Data: ' + angular.fromJson(data));
		});
	};
});

