'use strict';
angular.module('oga_web.gait_analysis', ["ngRoute", "ngMaterial", "ngMdIcons", "ui.bootstrap", "oga_web.patients"])
.config(['$routeProvider', function($routeProvider) {
	$routeProvider
	.when("/gait_analysis/patient/:id", {
		templateUrl: "gait_analysis/gait_analysis.html",
		controller: "gaitAnalysisCtrl", 
		resolve: {
			patient: function(ogaFacade, $route) {
				var id = $route.current.params.id;
				return ogaFacade.getPatient(id);
			}
		}
	});
}])
.controller('gaitAnalysisCtrl', function ($rootScope, $scope, $location, patient){
	$scope.patient = patient.data;
	$scope.isAdding = false;
	$scope.addGaitData = function() {
		$scope.isAdding = true;
	};
	$scope.setFile = function (element) {
		$scope.currentFile = element.files[0];
	};
	$scope.uploadFile = function () {
		var formData = new FormData();
		formData.append('file', $scope.currentFile);
		$scope.isAdding = false;
	};
	$scope.cancel = function() {
		//reload view
		$location.path('/gait_analysis/patient/' + $scope.patient.id + '/');
	}
	
});
