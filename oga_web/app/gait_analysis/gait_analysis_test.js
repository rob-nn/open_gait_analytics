'use strict';
describe('Gait Analysis controller specification', function () {
	var $scope, mockedSamples, $httpBackend, $location, webapi;
	var $controller;
	var gait_sample;
	var patient;

	beforeEach(module('oga_web.gait_analysis'));
	beforeEach(module('oga_web.oga_facade'));

	beforeEach(inject(function($rootScope, _$controller_, _$httpBackend_, _$location_, urlApi){
		$scope = $rootScope.$new();
		$httpBackend = _$httpBackend_;
		$location = _$location_;
		webapi = urlApi.urlString();
		$controller = _$controller_;
		patient = buildMockedPatients().getPatients()[0];
		patient.gait_samples = [];
		gait_sample = {id:0, date: new Date(2010, 1, 1), description: 'testing'};
		patient.gait_samples.push(gait_sample);
		var patient_ = {data:patient};
		$controller('gaitAnalysisCtrl', {$scope:$scope, patient:patient_});
	}));

	var checkInitialState = function(){
		expect($scope.patient).toEqual(patient);	
		expect($scope.isAdding).toEqual(false);
		expect($scope.gaitSampleEnabled).toEqual(true);
		expect($scope.gait_sample).toBeDefined();
		expect($scope.patient.gait_samples).toBeDefined();
		expect($scope.isShowMarkers).toBe(false);
		expect($scope.positionalsData).toBe(null);
	};

	it('Test initial state without gait samples', function () {
		$scope.patient.gait_samples.pop();
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
		expect($scope.patient.gait_samples).toBeDefined();
		expect($scope.isShowMarkers).toEqual(false);
		expect($scope.positionalsData).toEqual(null);
	});
	it('Test add gait sample state after edit markers', function(){
		$scope.addGaitData();
		expect($scope.isShowMarkers).toEqual(false);
		$scope.showMarkers();
		$scope.addGaitData();
		expect($scope.isShowMarkers).toEqual(false);
	});

	it('Test add new gait sample', function() {
		$httpBackend.whenPUT(webapi + 'patients/').respond(function(method, url, data, headers){
			var d = JSON.parse(data);
			expect(d.gait_samples).toBeDefined();
			expect(d.gait_samples.length).toEqual(1);
			return [204, angular.fromJson(data), {}];
		});
		$httpBackend.whenGET(webapi + 'gait_sample/positional_data/0/0/').respond(function(){
			return [404, {}, {}];
		});
		$scope.addGaitData();
		delete $scope.patient.gait_samples;
		expect($scope.patient.gait_samples).toBeUndefined();
		$scope.saveSample();
		$httpBackend.flush();
		expect($scope.patient.gait_samples).toBeDefined();
		expect($scope.patient.gait_samples.length).toEqual(1);
		expect($scope.isAdding).toBe(false);
		expect($scope.gaitSampleEnabled).toBe(true);
	});

	it('Test save a gait sample.', function(){
		$httpBackend.whenPUT(webapi + 'patients/').respond(function(method, url, data, headers){
			var d = JSON.parse(data);
			expect(d.gait_samples).toBeDefined();
			expect(d.gait_samples.length).toEqual(1);
			return [204, angular.fromJson(data), {}];
		});
		$httpBackend.whenPUT(webapi + 'gait_sample/positionals_data/').respond(function(method, url, data, headers){
			return [200, {}, {}];
		});
		$httpBackend.whenGET(webapi + 'gait_sample/positional_data/0/0/').respond(function(){
			return [200, {_id:11}, {}];
		});
		expect($scope.isAdding).toBe(false);
		$scope.showGaitSample(gait_sample);
		$httpBackend.flush();   
		expect($scope.positionalsData).toBeDefined();
		$scope.saveSample();
		$httpBackend.flush();   
		expect($scope.isAdding).toBe(false);
		expect($scope.gaitSampleEnabled).toBe(true);
		expect($scope.positionalsData).toBeDefined();
		expect($scope.positionalsData._id).toBeDefined();
		expect($scope.positionalsData._id).toBe(11);
	});


	it('Test gait sample is undefined and there are gait samples', function(){
		expect($scope.gait_sample).toBeDefined(); 
	});

	it('Test show gait sample.', function(){
		$scope.showGaitSample(gait_sample);	
		expect($scope.patient).toEqual(patient);	
		expect($scope.isAdding).toEqual(false);
		expect($scope.gaitSampleEnabled).toEqual(true);
		expect($scope.gait_sample).toEqual(gait_sample);
		expect($scope.patient.gait_samples.length).toBe(1);
		expect($scope.isShowMarkers).toBe(false);
	});

	it ('Test upload a gait sample', function() {
		var files = [new File([''], 'mocks.txt')];
		var mock_data = {'id_patient': 0, 'gait_sample_index': 0, 'frame_rate': 315, 'frames': 2000, 'number_marks': 20, 'original_filename': 'mocks.txt'};
		$httpBackend.whenPOST(webapi + 'gait_sample/upload/0/0/').respond(function(method, url, data, headers) {
			expect(data).toBeDefined();
			return [200, mock_data, {}];
		});
		$httpBackend.whenGET(webapi + 'gait_sample/positional_data/0/0/').respond(function(){
			return [200, {_id:11}, {}];
		});
		$scope.upload(files);
		$httpBackend.flush();
		expect($scope.gait_sample).toBeDefined();
		expect($scope.positionalsData).toNotBe(null);
		expect($scope.positionalsData.original_filename).toBe('mocks.txt');
	});

	it('Test showmarkers', function () {
		$scope.showMarkers()
		expect($scope.isShowMarkers).toBe(true);
	});

});
