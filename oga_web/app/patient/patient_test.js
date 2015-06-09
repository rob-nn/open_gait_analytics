'use strict'

describe('Patient controller specification.', function() {
	var $scope
	beforeEach(module('oga_web.patient'));
	beforeEach(inject( function ($controller, $rootScope){
		$scope = $rootScope.$new();
	});

	it ('Function save is present', function() {
		expect($scope.save).to
	});
