'use strict';
angular.module('oga_web.patients', ["ngRoute", "ngMaterial", "ngMdIcons", 'oga_web.oga_facade'])
.config(['$routeProvider', function($routeProvider) {
	$routeProvider
	.when("/patients", {
		templateUrl: "patients/patients.html",
		controller: "patientsCtrl", 
		resolve: {
			patients: function(patientsFacade) {
				return patientsFacade.getPatients();
			}
		}
	});
}])
.constant("webapi", {
	url:  'http://localhost:8000/'
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

});
