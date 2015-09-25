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
.controller('cmacCtrl', function($scope, patientsFacade, positionalsDataFacade, simulationFacade, $mdToast) {
	//functions
	$scope.runCmacTraining = runCmacTraining;
	$scope.showInputSignals = showInputSignals;
	$scope.showQuantization = showQuantization;
	$scope.showQuantizationAngles = showQuantizationAngles;
	$scope.showSamples = showSamples;
	//Atributes
	$scope.activationsNumber = null;
	$scope.idPatient = null;
	$scope.indexSample = null;
	$scope.iterationsNumber = null;
	$scope.markers = null;
	$scope.outputIndex = null;
	$scope.outputs = null;
	$scope.patients = null;
	$scope.pos = null; //using angles
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
					var marker = {index: index, description: data.markers[index]};
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
			generateOutputSignals();
		}).error(function(data, status, headers, config){
			$mdToast.show(
				$mdToast.simple()
				.content("Error bringing positionals data!")
				.position('bottom right')
				.hideDelay(3000)
			);
		}); 
	};

	function generateOutputSignals() {
		var outputs = [];
		var i = 0;
		for (var index in $scope.markers) {
			var marker = $scope.markers[index];
			var output = null;
			output = {
				index: i,
				type: 0, //0 marker, 1 angle
				description: 'marker - ' + marker.description + ' - x',
				_id: marker.index,
				component: 'x', //x, y , z to markers or a, v to angles
				component_description: 'x'
			};
			outputs.push(output);
			i++;
			output = {
				index: i,
				type: 0, //0 marker, 1 angle
				description: 'marker - ' + marker.description + ' - y',
				_id: marker.index,
				component: 'y', //x, y , z to markers or a, v to angles
				component_description: 'y'
			};
			outputs.push(output);
			i++;
			output = {
				index: i,
				type: 0, //0 marker, 1 angle
				description: 'marker - ' + marker.description + ' - z',
				_id: marker.index,
				component: 'z', //x, y , z to markers or a, v to angles
				component_description: 'z'
			};
			outputs.push(output);
			i++;
		}
		for (var index in $scope.pos.angles) {
			var angle = $scope.pos.angles[index];
			var output = null;
			output = {
				index: i,
				type: 1, //0 marker, 1 angle
				description: 'angle - ' + angle.description + ' - angles',
				_id: index,
				component: 'a', //x, y , z to markers or a, v to angles
				component_description: 'angles'
			};
			outputs.push(output);
			i++;
			output = {
				index: i,
				type: 1, //0 marker, 1 angle
				description: 'angle - ' + angle.description + ' - angular velocities',
				_id: index,
				component: 'v', //x, y , z to markers or a, v to angles
				component_description: 'angular velocities'
			};
			outputs.push(output);
			i++;
		}
		$scope.outputs = outputs;
	}

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

	function runCmacTraining(){
		var output = null;
		for (var index in $scope.outputs) {
			output = $scope.outputs[index];
			if (output.index = $scope.outputIndex) break;
		}
		simulationFacade.runCmacTraining($scope.idPatient, $scope.pos._id.$oid, $scope.activationsNumber, $scope.iterationsNumber, output, 
				$scope.markers, $scope.pos.angles).success(function(data, status, headers, config){
			
		}).error(function(data, status, headers, config){
			var msg = "Error training CMAC.";
			if (data.error) 
				msg = msg + " " + data.error;
			$mdToast.show(
				$mdToast.simple()
				.content(msg)
				.position('bottom right')
				.hideDelay(3000)
			);
		});
	}
});

