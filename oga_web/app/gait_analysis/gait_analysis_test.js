'use strict';
describe('Gait Analysis controller specification', function () {
	var $scope, mockedSamples, $httpBackend, webapi, gaitSamplesFacade;
	var $controller;
	var gait_sample;
	var patient;

	beforeEach(module('oga_web.gait_analysis'));
	beforeEach(module('oga_web.oga_facade'));

	beforeEach(inject(function($rootScope, _$controller_, _$httpBackend_, _webapi_, _gaitSamplesFacade_){
		$scope = $rootScope.$new();
		$httpBackend = _$httpBackend_;
		webapi = _webapi_;
		gaitSamplesFacade = _gaitSamplesFacade_;
		$controller = _$controller_;
		patient = buildMockedPatients().getPatients()[0];
		patient.samples = [];
		gait_sample = {id:0, date: new Date(2010, 1, 1), description: 'testing'};
		patient.samples.push(gait_sample);
		var patient_ = {data:patient};
		$controller('gaitAnalysisCtrl', {$scope:$scope, patient:patient_});
	}));

	var checkInitialState = function(){
		expect($scope.patient).toEqual(patient);	
		expect($scope.isAdding).toEqual(false);
		expect($scope.gaitSampleEnabled).toEqual(true);
		expect($scope.gait_sample).toBeDefined();
		expect($scope.patient.samples).toBeDefined();
	};

	it('Test initial state without gait samples', function () {
		$scope.patient.samples.pop();
		$controller('gaitAnalysisCtrl', {$scope:$scope, patient:{data: $scope.patient}});
		expect($scope.gait_sample).toBeDefined();
		expect($scope.gaitSampleEnabled).toEqual(false);
	});

	it('Test initial state', function() {
		checkInitialState();
	 });

	it('Test add gait sample state', function(){
		$scope.addGaitData();
		expect($scope.patient).toEqual(patient);	
		expect($scope.isAdding).toEqual(true);
		expect($scope.gaitSampleEnabled).toEqual(false);
		expect($scope.gait_sample).toBeDefined();
		expect($scope.gait_sample.patient).toEqual($scope.patient.id);
		expect($scope.patient.samples).toBeDefined();
	});


	it('Test add new gait sample', function() {
		$httpBackend.whenPOST(webapi.url + 'gait_samples/').respond(function(){
			$scope.patient.samples.push(gait_sample);
			return [201, gait_sample, {}];	
		});
		$scope.addGaitData();
		$scope.saveSample();
		$httpBackend.flush();
		expect($scope.patient.samples.length).toEqual(2);
	});

	it('Test gait sample is undefined and thera gait samples', function(){
		expect($scope.gait_sample).toBeDefined(); 
	});


	it('Test show gait sample.', function(){
		$scope.showGaitSample(gait_sample);	
		expect($scope.patient).toEqual(patient);	
		expect($scope.isAdding).toEqual(false);
		expect($scope.gaitSampleEnabled).toEqual(true);
		expect($scope.gait_sample).toEqual(gait_sample);
		expect($scope.patient.samples.length).toBe(1);
	});

	it('Test save a gait sample.', function(){
		$httpBackend.whenPUT(webapi.url + 'gait_samples/0/').respond(function(method, url, data, headers){
			$scope.patient.samples[0].description = 'new description';
			return [204, angular.fromJson(data), {}];
		});
		$scope.showGaitSample(gait_sample);
		$scope.saveSample();
		$httpBackend.flush();   
		expect($scope.patient.samples[0].description).toEqual('new description');
	});

});
