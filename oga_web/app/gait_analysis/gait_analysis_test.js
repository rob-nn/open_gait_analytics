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
		$scope.addGaitData();
		delete $scope.patient.gait_samples;
		expect($scope.patient.gait_samples).toBeUndefined();
		$scope.saveSample();
		$httpBackend.flush();
		expect($scope.patient.gait_samples).toBeDefined();
		expect($scope.patient.gait_samples.length).toEqual(1);
		expect($location.path()).toBe('/gait_analysis/patient/' + $scope.patient._id.$oid + '/');
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
		expect($scope.patient.gait_samples.length).toBe(1);
	});

	it('Test save a gait sample.', function(){
		$httpBackend.whenPUT(webapi + 'gait_samples/0/').respond(function(method, url, data, headers){
			$scope.patient.samples[0].description = 'new description';
			return [204, angular.fromJson(data), {}];
		});
		$scope.showGaitSample(gait_sample);
		$scope.saveSample();
		//$httpBackend.flush();   
		//expect($scope.patient.samples[0].description).toEqual('new description');
	});
	
	it ('Test upload a gait sample', function() {
		var files = [new File([''], 'mocks.txt')];
		var mock_data = {'frame_rate': 315, 'frames': 2000, 'number_marks': 20, 'original_filename': 'mocks.txt'};
		$httpBackend.whenPOST(webapi + 'gait_sample/upload/').respond(function(method, url, data, headers) {
			expect(data).toBeDefined();
			return [200, mock_data, {}];
		});
		$scope.upload(files);
		$httpBackend.flush();
		expect($scope.gait_sample.data).toBeDefined();
		expect($scope.gait_sample.data).toEqual(mock_data);
	});

	it('Test showmarkers', function () {
		$scope.showMarkers()
		expect($scope.isShowMarkers).toBe(true);
	});

});
