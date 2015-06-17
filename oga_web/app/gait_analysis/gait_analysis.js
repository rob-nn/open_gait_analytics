'use strict';
angular.module('oga_web.gait_analysis', ["ngFileUpload", "ngRoute", "ngMaterial", "ngMdIcons", "oga_web.oga_facade"])
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
.controller('gaitAnalysisCtrl', function (
	$rootScope, 
	$scope, 
	$location, 
	patient, 
	Upload,
	gaitSamplesFacade, 
	$timeout, 
	$mdSidenav, 
	$mdUtil, 
	$log, 
	urlApi){
	$scope.upload = function(files){
		if (files && files.length) {
			var file = files[0];
			Upload.upload({
				url: urlApi.urlString() + 'gait_sample/upload/',
				fields: {'username': 'teting'},
				file: file
			}).progress(function (evt){
				var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
				console.log('progress: ' + progressPercentage + '% ' + evt.config.file.name);
			}).success(function(data, status, headers, config){
				$scope.gait_sample.data = data;
				console.log('file ' + config.file.name + 'uploaded. Response: ' + data);
			}).error(function(data, status, headers, config){
				console.log('Error: ' + status);
			});
		}
	};
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
	$scope.showGaitSample = function(gait_sample) {
		$scope.gait_sample = gait_sample;
		$scope.gaitSampleEnabled = true;
		$scope.isAdding = false;
	}
	if ($scope.gait_sample == null){
		if ($scope.patient.samples && $scope.patient.samples.length > 0){
			$scope.showGaitSample($scope.patient.samples[0]);
		}
	}
	else {
		$scope.showGaitSample($scope.gait_sample);
	}
	$scope.addGaitData = function() {
		$scope.gait_sample = {patient: $scope.patient.id, date:new Date(), description:null};
		$scope.isAdding = true;
		$scope.gaitSampleEnabled = false;
	};
	$scope.setFile = function (element) {
		$scope.currentFile = element.files[0];
	};
	$scope.cancel = function() {
		$location.path('/gait_analysis/patient/' + $scope.patient.id + '/');
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
				var x;
				x = 'abc';
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
