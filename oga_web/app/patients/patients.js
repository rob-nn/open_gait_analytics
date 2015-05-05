'use strict';
angular.module('oga_web.patients', ["ngRoute", "ngMaterial", "ngMdIcons", "ui.bootstrap"])
.config(['$routeProvider', function($routeProvider) {
	$routeProvider
	.when("/patients", {
		templateUrl: "patients/patients.html",
		controller: "patientsCtrl", 
		resolve: {
			patients: function(ogaFacade) {
				return ogaFacade.getPatients();
			}
		}
	});
}])
.constant("webapi", {
	url:  'http://localhost:8000/patients/'
})
.controller('patientsCtrl', function ($rootScope, $scope, $location, patients){
	$scope.showListViewIcon = true;
	$scope.patients = patients.data;
	$scope.showListView = function() {
		$scope.showListViewIcon = false;
	};
	$scope.showGridView = function() {
		$scope.showListViewIcon = true;
	};
	$scope.createPatient = function(){
		$location.path('/patient_new');
	};
	$scope.openGaitAnalysis = function (patient_id) {
		$location.path('/gait_analysis/patient/' + patient_id + '/');
	};

})
.factory("ogaFacade", function($http, webapi){
	var _getPatient = function(id) {
		return $http.get(webapi.url + id + '/');
	}
	var _getPatients = function() {
		return $http.get(webapi.url);
	};
	var _addPatient = function(patient) {
		return $http.post(webapi.url, patient);
	};
	return {
		getPatients: _getPatients,
		getPatient: _getPatient,
		addPatient: _addPatient
	};
});





