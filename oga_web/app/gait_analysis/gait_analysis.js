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
	});
}])
.controller('gaitAnalysisCtrl', function (
	$rootScope, 
	$scope, 
	$location, 
	patient, 
	Upload,
	$timeout, 
	$mdSidenav, 
	$mdUtil, 
	$log, 
	urlApi,
	patientsFacade){

	$scope.patient = patient.data;
	$scope.isAdding = false;
	$scope.gaitSampleEnabled = false;
	$scope.gait_sample = null;
	$scope.isShowMarkers = false;

	$scope.showGraphic = showGraphic;
	
	function showGraphic (selected_marker) {
		marker = $scope.gait_sample.data.markers[selected_marker];
		
	}

	$scope.showGaitSample = function(gait_sample) {
		$scope.gait_sample = gait_sample;
		$scope.gaitSampleEnabled = true;
		$scope.isAdding = false;
	}
	if ($scope.gait_sample == null){
		if ($scope.patient.gait_samples && $scope.patient.gait_samples.length > 0){
			$scope.showGaitSample($scope.patient.gait_samples[0]);
		}
	}
	else {
		$scope.showGaitSample($scope.gait_sample);
	}
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
	$scope.addGaitData = function() {
		$scope.gait_sample = {date:new Date(), description:null};
		$scope.isAdding = true;
		$scope.gaitSampleEnabled = false;
		$scope.isShowMarkers = false;
	};
	$scope.setFile = function (element) {
		$scope.currentFile = element.files[0];
	};
	$scope.cancel = function() {
		$location.path('/gait_analysis/patient/' + $scope.patient.id + '/');
	}
	$scope.saveSample= function(){
		if ($scope.isAdding){
			if (typeof($scope.patient.gait_samples) === 'undefined')
				$scope.patient.gait_samples = [];
			$scope.patient.gait_samples.push($scope.gait_sample);
		}
		patientsFacade.updatePatient($scope.patient).success(function (data, status, headers, config) {
			$location.path('/gait_analysis/patient/' + $scope.patient._id.$oid  + '/');
		})
		.error(function(data, status, headers, config){
			$scope.patient.gait_samples.pop();
			//alert('Error: '+status + ' Data: ' + angular.fromJson(data));
		});
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
	$scope.showMarkers= function () {
		$scope.isShowMarkers = !$scope.isShowMarkers;
	}
});
