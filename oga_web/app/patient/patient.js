'use strict';
angular.module('oga_web.patient', ["ngMessages", "ngRoute", "ngMaterial", "ngMdIcons", "oga_web.oga_facade"])
.config(['$routeProvider', function($routeProvider) {
	$routeProvider.when("/patient_new", {
		templateUrl: "patient/patient.html",
		controller: "patientNewCtrl",
	});
	$routeProvider.when("patient/:id", {
		templateUrl: "patient/patient_detail.html",
		controller: "gaitAnalysisCtrl", 
		resolve: {
			patient: function(patientsFacade, $route) {
				var id = $route.current.params.id;
				return patientsFacade.getPatient(id);
			}
		}

	});
}])
.controller('patientNewCtrl', function($scope, patientsFacade, $location){
	$scope.patient = {};
	$scope.save = function(){
		patientsFacade.addPatient($scope.patient).success(function (data, status, headers, config) {
			$location.path('/patients');
		})
		.error(function(data, status, headers, config){
			alert('Error: '+status + ' Data: ' + angular.fromJson(data));
		});
	};
}). 
controller('patientEditCtrl', function($scope, $mdToast, patientsFacade) {
	$scope.save = save;

	function save() {
		patientsFacade.updatePatient($scope.patient).success(function (data, status, headers, config) {
			makeToast("Saved");
		}).error(function(data, status, headers, config){
			alert('Error: '+status + ' Data: ' + angular.fromJson(data));
		});
	};		
	
	function makeToast(str) {
		$mdToast.show(
			$mdToast.simple()
			.content(str)
			.position('bottom right')
			.hideDelay(3000)
		);
	};

});
