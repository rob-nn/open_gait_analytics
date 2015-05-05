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

describe('Patients ogaFacade specification', function () {
	var ogaFacade, $httpBackend, mockedPatients, webapi;
	beforeEach(module('oga_web.patients'));
	beforeEach(inject(function(_ogaFacade_, _$httpBackend_, _webapi_){
		ogaFacade = _ogaFacade_;
		$httpBackend = _$httpBackend_;
		webapi = _webapi_;
		mockedPatients = buildMockedPatients();
	}));

	it ('Must have patients', function(){
		$httpBackend.whenGET(webapi.url).respond(function(){
			return [200, mockedPatients.getPatients(), {}];	
		});
		ogaFacade.getPatients().success(function(data, status){
			expect(data).toBeDefined();
			expect(data.length).toEqual(2);
			expect(status).toEqual(200);
		});
		$httpBackend.flush();
	});;

	it('Must find patient with id = 1', function(){
		$httpBackend.whenGET(webapi.url + 1 + '/').respond(function(){
			var patient = mockedPatients.getPatient(1);
			return [200, patient, {}];
		});
		ogaFacade.getPatient(1).success(function(data, status){
			expect(data).toEqual(mockedPatients.getPatient(1));
			expect(status).toEqual(200);
		});
		$httpBackend.flush();
	});

	it ('Must add a patient', function(){
		var patient = {name : 'Mary', birth:new Date(1984, 12, 1)};
		$httpBackend.whenPOST(webapi.url).respond(function(){
			var id = mockedPatients.addPatient(patient);
			return [201, mockedPatients.getPatient(id), {}];	
		});
		ogaFacade.addPatient(patient).success(function(data, status){
			expect(data).toEqual(patient);
			expect(status).toEqual(201);
		});
		$httpBackend.flush();

	});
});

var buildMockedPatients = function () {
	var _patients =[
		{ 
			name: 'Roberto A. Lima',
			birth: new Date(1977, 11, 19)
		},
		{
			name: 'Joseph Smith',
			birth: new Date(1980, 1, 1)
		}
	];
	var _id = function(id) {return id -1;};
	var _getPatient = function (id) {return _patients[_id(id)];};
	var _getPatients = function () {return _patients;};
	var _addPatient = function(patient) {
		return _patients.push(patient);
	};

	return {
		getPatients : _getPatients,
		getPatient : _getPatient, 
		addPatient : _addPatient
	}

};

