'use strict';
angular.module('oga_web.patient', ["ngRoute", "ngMaterial", "ngMdIcons", "oga_web.oga_facade"])
.config(['$routeProvider', function($routeProvider) {
	$routeProvider.when("/patient_new", {
		templateUrl: "patient/patient.html",
		controller: "patientNewCtrl",
	})
}])
.controller('patientNewCtrl', function($scope, patientsFacade, $location){
	$scope.save = function(){
		patientsFacade.addPatient($scope.patient).success(function (data, status, headers, config) {
			$location.path('/patients');
		})
		.error(function(data, status, headers, config){
			alert('Error: '+status + ' Data: ' + angular.fromJson(data));
		});
	};
});
