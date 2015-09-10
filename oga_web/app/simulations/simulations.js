'use strict';
angular.module('oga_web.simulations', ["ngRoute", "ngMaterial", "ngMdIcons", "oga_web.oga_facade"])
.config(['$routeProvider', function($routeProvider) {
	$routeProvider
	.when("/simulations", {
		templateUrl: "simulations/simulations.html",
		controller: "simulationsCtrl" 
	});
}])
.controller('simulationsCtrl', function ($scope, $location){
	$scope.goBack = goBack;
	function goBack() {
		$location.path("/");
	};
})
.controller('cmacCtrl', function($scope, patientsFacade, positionalsDataFacade, $mdToast) {
	$scope.showSamples = showSamples;
	$scope.showInputSignals = showInputSignals;
	$scope.showQuantization = showQuantization;
	$scope.showQuantizationAngles = showQuantizationAngles;
	$scope.idPatient = null;
	$scope.markers = null;
	$scope.indexSample = null;
	$scope.activationsNumber = null;
	$scope.iterationsNumber = null;
	$scope.trainingPercentual = null;
	patientsFacade.getPatients().success(function(data, status, headers, config){
		$scope.patients = data;
	}).error(function(data, status, headers, config){
		$mdToast.show(
			$mdToast.simple()
			.content("Error finding patients.")
			.position('bottom right')
			.hideDelay(3000)
		);
	});

	function showSamples() {
		$scope.markers = null;
		for(var index in $scope.patients) {
			var patient = $scope.patients[index];
			if (patient._id.$oid == $scope.idPatient) {
				$scope.patient = patient;
				if (patient.gait_samples != null && patient.gait_samples.length > 0) {
					$scope.samples = patient.gait_samples;	
				} else {
					$scope.markers = null;
					$scope.indexSample = null;
					$scope.samples = null;
					$mdToast.show(
						$mdToast.simple()
						.content("This patient haven't gait samples.")
						.position('bottom right')
						.hideDelay(3000)
					);
				}
				break;
			}
		}
	};
	
	function showInputSignals() {
		$scope.markers = null;
		positionalsDataFacade.getPositionalsData($scope.patient._id.$oid, $scope.indexSample).success(function(data, status, headers, config){
			$scope.pos = data;
			var markers = [];
			for (var index=0 ; index <  data.markers.length; index++) {
				if (data.markers[index] != null && data.markers[index].trim() != ""){
					var marker = {description: data.markers[index]};
				       markers.push(marker);	
				}
			}
			if (markers.length > 0) 
				$scope.markers = markers;
			else
				$mdToast.show(
					$mdToast.simple()
					.content("This gait sample haven't named markers!") 
					.position('bottom right')
					.hideDelay(3000)
				);
		}).error(function(data, status, headers, config){
			$mdToast.show(
				$mdToast.simple()
				.content("Error bringing positionals data!")
				.position('bottom right')
				.hideDelay(3000)
			);
		}); 
	};

	function showQuantization(index) {
		var marker = $scope.markers[index];
		if (marker.xCheckedForInput) 
			marker.showQX = true;
		else 
			marker.showQX = false;
		if (marker.yCheckedForInput) 
			marker.showQY = true;
		else 
			marker.showQY = false;
		if (marker.zCheckedForInput) 
			marker.showQZ = true;
		else 
			marker.showQZ = false;
	};

	function showQuantizationAngles(index) {
		var angle = $scope.pos.angles[index];
		if (angle.anglesCheckedForInput)
			angle.showAngles = true;
		else
			angle.showAngles = false;
		if (angle.angVelCheckedForInput)
			angle.showAngVel = true;
		else
			angle.showAngVel = false;


	}
});

