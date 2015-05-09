'use strict';

describe('Patients controller specification.', function(){
	var $scope, mockedPatients;
	
	beforeEach(module('oga_web.patients'));
	beforeEach(inject(function ($controller, $rootScope) {
		mockedPatients = buildMockedPatients();	
		$scope = $rootScope.$new();
		var patients = {data: mockedPatients.getPatients()};
		$controller('patientsCtrl', {$scope:$scope, patients : patients});
	}));

	it('List View option must be shown.', function(){
		expect($scope.showListViewIcon).toBe(true);
	});

	it('Show grid view must show list view icon.', function() {
		$scope.showGridView();
		expect($scope.showListViewIcon).toBe(true);
	});

	it('Show list view must hide show list view icon.', function() {
		$scope.showListView();
		expect($scope.showListViewIcon).toBe(false);
	});
	
	it ('Must have patients.', function () {
       		expect($scope.patients).toBeDefined();
       		expect($scope.patients.length).toEqual(2);
	}); 
});
