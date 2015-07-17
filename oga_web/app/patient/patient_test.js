'use strict'

describe('Patient controller specification.', function() {
	var $scope, $httpBackend, $location, webapi
	beforeEach(module('oga_web.patient'));
	beforeEach(inject( function ($controller, $rootScope, _$location_, _$httpBackend_, urlApi){
		$httpBackend = _$httpBackend_;
		$scope = $rootScope.$new();
		$controller('patientNewCtrl', {$scope:$scope});
		webapi = urlApi.urlString();
		$location = _$location_
	}));

	it ('Function save is present', function() {
		expect($scope.save).toBeDefined();
	});

	it('Add a new patient', function() {
		$httpBackend.whenPOST(webapi + 'patients/').respond(function(method, url, data, headers){
			
			return [201, {}, {}];	
		});
		$scope.save();
		$httpBackend.flush();
		expect($location.path()).toBe('/patients');
	});

});
