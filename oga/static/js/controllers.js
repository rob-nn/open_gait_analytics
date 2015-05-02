oga.controller('patientsCtrl', function ($rootScope, $scope, $location, patients){
	$scope.showListViewIcon = true;
	$scope.patients = patients.data;
	$scope.showListView = function() {
		$scope.showListViewIcon = false;
	};
	$scope.showGridView = function() {
		$scope.showListViewIcon = true;
	};
	$scope.createPatient = function(){
		$location.path('/patients_new');
	};
});

oga.controller('patientCtrl', function($scope) {
});

oga.controller('patientNewCtrl', function($scope, ogaFacade, $location){
	$scope.open = function($event) {
		$event.preventDefault();
		$event.stopPropagation();
		$scope.opened = true;
	};
	$scope.save = function(){
		ogaFacade.addPatient($scope.patient).success(function (data, status, headers, config) {
			$location.path('/patients');
		})
		.error(function(data, status, headers, config){
			alert('Error: '+status + ' Data: ' + angular.fromJson(data));
		});
	};
});
