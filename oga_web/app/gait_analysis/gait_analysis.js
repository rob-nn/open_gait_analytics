'use strict';
angular.module('oga_web.gait_analysis', ["ngRoute", "ngMaterial", "ngMdIcons", "oga_web.oga_facade"])
.config(['$routeProvider', function($routeProvider) {
	$routeProvider
	.when("/gait_analysis/patient/:id", {
		templateUrl: "gait_analysis/gait_analysis.html",
		controller: "gaitAnalysisCtrl", 
		resolve: {
			patient: function(patientsFacade, $route) {
				var id = $route.current.params.id;
				return patientsFacade.getPatient(id);
			}
		}
	})
}])
.controller('gaitAnalysisCtrl', function ($rootScope, $scope, $location, patient, gaitSamplesFacade, $timeout, $mdSidenav, $mdUtil, $log){
	$scope.patient = patient.data;
	if ($scope.patient.samples) {
		for(var i=0; i < $scope.patient.samples.length; i++){
			$scope.patient.samples[i].date = new Date($scope.patient.samples[i].date);
		}
	}
	$scope.isAdding = false;
	$scope.gaitSampleEnabled = false;
	$scope.gait_sample = null;
	$scope.gait_cycles = [
		{id:1, description: 'xxxxxxx', initial_contact_frame:'10', end_terminal_swing_frame:'100'},
	];

	$scope.addGaitData = function() {
		$scope.gait_sample = {patient: $scope.patient.id, date:new Date(), description:null};
		$scope.isAdding = true;
		$scope.gaitSampleEnabled = false;
	};
	$scope.setFile = function (element) {
		$scope.currentFile = element.files[0];
	};
	$scope.cancel = function() {
		//reload view
		$location.path('/gait_analysis/patient/' + $scope.patient.id + '/');
	}
	$scope.showGaitSample = function(gait_sample) {
		$scope.gait_sample = gait_sample;
		$scope.gaitSampleEnabled = true;
		$scope.isAdding = false;
	}
	$scope.saveSample= function(){
		if ($scope.isAdding){
			gaitSamplesFacade.addGaitSample($scope.gait_sample).success(function (data, status, headers, config) {
				$location.path('/gait_analysis/patient/' + $scope.patient.id + '/');
			})
			.error(function(data, status, headers, config){
				alert('Error: '+status + ' Data: ' + angular.fromJson(data));
			});
		} else {
			gaitSamplesFacade.updateGaitSample($scope.gait_sample).success(function(data, status, headers, config) {

			})
			.error(function(data, status, headers, config){
				alert('Error: '+status + ' Data: ' + angular.fromJson(data));
			});

		}

	};
	$scope.toggleLeft = buildToggler('left');
	/**
	* Build handler to open/close a SideNav; when animation finishes
	* report completion in console
	*/
	function buildToggler(navID) {
		var debounceFn =  $mdUtil.debounce(function(){
			$mdSidenav(navID)
			.toggle()
			.then(function () {
				//$log.debug("toggle " + navID + " is done");
			});
		},300);
		return debounceFn;
	}
	$scope.close = function () {
		$mdSidenav('left').close()
		.then(function () {
			//$log.debug("close LEFT is done");
		});
	};
});
