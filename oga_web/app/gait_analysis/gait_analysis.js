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
	$sce,
	patient, 
	Upload,
	$timeout, 
	$mdSidenav, 
	$mdUtil, 
	$mdToast,
	$log,
        $mdDialog,	
	urlApi,
	patientsFacade,
	positionalsDataFacade){

	$scope.patient = patient.data;
	$scope.isAdding = false;
	$scope.isAddingNewAngle = false;
	$scope.gaitSampleEnabled = false;
	$scope.gait_sample = null;
	$scope.positionalsData = null;
	$scope.isShowMarkers = false;
	$scope.isShowAngles = false;
	$scope.angle = null;

	$scope.addNewAngle = addNewAngle;
	$scope.cancelNewAngle = cancelNewAngle;
	$scope.showGraphic = showGraphic;
	$scope.showGaitSample = showGaitSample;
	$scope.upload = upload; 
	$scope.addGaitData = addGaitData;
	$scope.setFile = setFile;
	$scope.cancel = cancel;
	$scope.confirmDeletion = confirmDeletion;
	$scope.saveNewAngle = saveNewAngle;
	$scope.saveSample= saveSample;
	$scope.showMarkers = showMarkers;
	$scope.showAngles = showAngles;
	$scope.goBack = goBack;

	if ($scope.gait_sample == null){
		if ($scope.patient.gait_samples && $scope.patient.gait_samples.length > 0){
			$scope.showGaitSample($scope.patient.gait_samples[0]);
		}
	}
	else {
		$scope.showGaitSample($scope.gait_sample);
	}

	function addNewAngle() {
		$scope.isAddingNewAngle = true;
	}
	
	function cancelNewAngle() {
		$scope.angle = null;
		$scope.isAddingNewAngle = false;
		$scope.angle = null;
	}

	function confirmDeletion(ev) {
		// Appending dialog to document.body to cover sidenav in docs app
		var confirm = $mdDialog.confirm()
		.title('Would you like to delete gait sample ' + $scope.gait_sample.description + '?')
		.content('')
		.ariaLabel('Gait Sample Deletion')
		.ok('Ok')
		.cancel('Cancel')
		.targetEvent(ev);
		$mdDialog.show(confirm).then(function() {
			positionalsDataFacade.deletePositionalsData($scope.positionalsData._id.$oid).success(function(data, status, headers, config) {	
				$location.path('/gait_analysis/patient/' + $scope.patient._id.$oid + '/');
				make_toast('Deleted');
			})
			.error(function (data, status, headers, config){
				make_toast('Deletion failed');
			});
		}, function() {
			make_toast('Canceled');
		});
	};
	function saveNewAngle() {
		if (!$scope.positionalsData.angles) {
			$scope.positionalsData.angles=[];
		}
		$scope.positionalsData.angles.push($scope.angle);
		$scope.angle = null;
		$scope.isAddingNewAngle = false;
	}

	function showGraphic (selected_marker) {
		positionalsDataFacade.plotMarker($scope.positionalsData._id.$oid, selected_marker).success(function (data, status, headers, config) {
			var myWindow = window.open("empty.html", "MsgWindow", "width=750, height=750");
			myWindow.document.write(data);
		}).error(function(data, status, headers, config){
				console.log('Error: ' + status);
		});
	}

	function showGaitSample(gait_sample) {
		if (gait_sample.date) {
			var date = new Date(gait_sample.date);
			gait_sample.date = date;
		}
		$scope.gait_sample = gait_sample;
		$scope.gaitSampleEnabled = true;
		$scope.isAdding = false;
		var sample_index = $scope.patient.gait_samples.indexOf($scope.gait_sample);
		positionalsDataFacade.getPositionalsData($scope.patient._id.$oid, sample_index).success(function(data, status, headers, config){
			$scope.positionalsData = data;			
		}).error(function(data, status, headers, config){
			$scope.positionalsData = null;
		});
		$scope.isShowMarkers = false;
		$scope.isShowAngles = false;
		$scope.isAddingNewAngle = false;
	}

	function upload (files){
		if (files && files.length) {
			var file = files[0];
			Upload.upload({
				url: urlApi.urlString() + 'gait_sample/upload/' + $scope.patient._id.$oid + '/'+ $scope.patient.gait_samples.indexOf($scope.gait_sample) + '/',
				fields: {'username': 'teting'},
				file: file
			}).progress(function (evt){
				var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
				console.log('progress: ' + progressPercentage + '% ' + evt.config.file.name);
			}).success(function(data, status, headers, config){
				$scope.positionalsData = data;
				console.log('file ' + config.file.name + 'uploaded.');
			}).error(function(data, status, headers, config){
				console.log('Error: ' + status);
			});
		}
	};

	function addGaitData() {
		var newDate = new Date();
		newDate =new Date(newDate.getFullYear(), newDate.getMonth(), newDate.getDate());
		$scope.gait_sample = {date:newDate, description:null};
		$scope.positionalsData = null;
		$scope.isAdding = true;
		$scope.gaitSampleEnabled = false;
		$scope.isShowMarkers = false;
		$scope.isShowAngles = false;
	};
	function setFile(element) {
		$scope.currentFile = element.files[0];
	};
	function cancel() {
		$location.path('/gait_analysis/patient/' + $scope.patient._id.$oid + '/');
	}
	function goBack() {
		$location.path('/');
	}
	function saveSample(){
		if ($scope.isAdding){
			if (typeof($scope.patient.gait_samples) === 'undefined')
				$scope.patient.gait_samples = [];
			$scope.patient.gait_samples.push($scope.gait_sample);
		}
		patientsFacade.updatePatient($scope.patient).success(function (data, status, headers, config) {
			if (!$scope.isAdding) 
				positionalsDataFacade.updatePositionalsData($scope.positionalsData).success(function(data, status, headers, config){
					var isShowMarkers = $scope.isShowMarkers;
					var isShowAngles = $scope.isShowAngles;
					$scope.showGaitSample($scope.gait_sample);
					$scope.isShowMarkers = isShowMarkers;	
					$scope.isShowAngles = isShowAngles;	
					make_toast('Saved');
				})
				.error(function(data, status, headers, config){
					make_toast('Failed');
				});
			
			else{
				$scope.isAdding = false;
				$scope.showGaitSample($scope.gait_sample);
				make_toast('Saved');
			}
			//$location.path('/gait_analysis/patient/' + $scope.patient._id.$oid  + '/');
		})
		.error(function(data, status, headers, config){
			$scope.patient.gait_samples.pop();
			alert('Error: '+status + ' Data: ' + angular.fromJson(data));
		});
	};
	function showMarkers() {
		$scope.isShowMarkers = !$scope.isShowMarkers;
		$scope.isShowAngles = false;
	}	
	function showAngles() {
		$scope.isShowAngles = !$scope.isShowAngles;
		$scope.isShowMarkers = false;
	}	
	
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
	function make_toast(str) {
		$mdToast.show(
			$mdToast.simple()
			.content(str)
			.position('bottom right')
			.hideDelay(3000)
		);
	};
});
