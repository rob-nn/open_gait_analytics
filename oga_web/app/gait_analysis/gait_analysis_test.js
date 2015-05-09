'use strict';
describe('Gait Analysis controller specification', function () {
	var $scope, mockedSamples, patient, $httpBackend, webapi, gaitSamplesFacade, mockedGaitSamples;
	var gait_sample;

	beforeEach(module('oga_web.gait_analysis'));
	beforeEach(module('oga_web.oga_facade'));
	beforeEach(inject(function($rootScope, $controller, _$httpBackend_, _webapi_, _gaitSamplesFacade_){
		patient = buildMockedPatients().getPatients()[0];
		mockedGaitSamples = buildMockedGaitSamples();
		$scope = $rootScope.$new();
		$httpBackend = _$httpBackend_;
		webapi = _webapi_;
		gaitSamplesFacade = _gaitSamplesFacade_;
		var patient_ = {data:patient};
		$controller('gaitAnalysisCtrl', {$scope:$scope, patient:patient_});
		gait_sample = {id:0, date: new Date(2010, 1, 1), description: 'testing'};
		var id = mockedGaitSamples.addGaitSample(gait_sample);   
		$scope.patient.samples = [];
		$scope.patient.samples.push(gait_sample);
	}));

	var checkInitialState = function(){
		expect($scope.patient).toEqual(patient);	
		expect($scope.isAdding).toEqual(false);
		expect($scope.gaitSampleEnabled).toEqual(false);
		expect($scope.gait_sample).toBeDefined();
		expect($scope.patient.samples).toBeDefined();
	};
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


	it('Test show gait sample.', function(){
		$scope.showGaitSample(gait_sample);	

		expect($scope.patient).toEqual(patient);	
		expect($scope.isAdding).toEqual(false);
		expect($scope.gaitSampleEnabled).toEqual(true);
		expect($scope.gait_sample).toEqual(gait_sample);
		expect($scope.patient.samples.length).toBe(1);
	});


	it('Test save a gait sample.', function(){
		$httpBackend.whenPUT(webapi.url + 'gait_samples/0/').respond(function(data){
			$scope.patient.samples[0].description = 'new description';
			return [204, angular.fromJson(data), {}];
		});
		$scope.showGaitSample(gait_sample);
		$scope.saveSample();
		$httpBackend.flush();   
		expect($scope.patient.samples[0].description).toEqual('new description');
	});
	
});
