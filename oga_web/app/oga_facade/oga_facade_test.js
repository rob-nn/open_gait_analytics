'use strict'

describe ('Patients Facade specification.',function(){
	var patientsFacade, $httpBackend, mockedPatients, webapi;
	beforeEach(module('oga_web.oga_facade'));
	beforeEach(inject(function(_patientsFacade_, _$httpBackend_, _webapi_){
		patientsFacade = _patientsFacade_;
		$httpBackend = _$httpBackend_;
		webapi = _webapi_;
		mockedPatients = buildMockedPatients();
	}));

	it ('Must have patients', function(){
		$httpBackend.whenGET(webapi.url + 'patients/').respond(function(){
			return [200, mockedPatients.getPatients(), {}];	
		});
		patientsFacade.getPatients().success(function(data, status){
			expect(data).toBeDefined();
			expect(data.length).toEqual(2);
			expect(status).toEqual(200);
		});
		$httpBackend.flush();
	});;

	it('Must find patient with id = 1', function(){
		$httpBackend.whenGET(webapi.url + 'patients/' + 1 + '/').respond(function(){
			var patient = mockedPatients.getPatient(1);
			return [200, patient, {}];
		});
		patientsFacade.getPatient(1).success(function(data, status){
			expect(data).toEqual(mockedPatients.getPatient(1));
			expect(status).toEqual(200);
		});
		$httpBackend.flush();
	});

	it ('Must add a patient', function(){
		var patient = {name : 'Mary', birth:new Date(1984, 12, 1)};
		$httpBackend.whenPOST(webapi.url + 'patients/').respond(function(){
			var id = mockedPatients.addPatient(patient);
			return [201, mockedPatients.getPatient(id), {}];	
		});
		patientsFacade.addPatient(patient).success(function(data, status){
			expect(data).toEqual(patient);
			expect(status).toEqual(201);
		});
		$httpBackend.flush();

	});
});


describe('Gait Samples facade specification.', function(){
	var $httpBackend, gaitSamplesFacade, webapi, mockedGaitSamples;
	var gaitSample;
	beforeEach(module('oga_web.oga_facade'));
	beforeEach(inject(function(_$httpBackend_, _gaitSamplesFacade_, _webapi_){
		$httpBackend = _$httpBackend_;
		gaitSamplesFacade = _gaitSamplesFacade_;
		webapi = _webapi_;
		mockedGaitSamples = buildMockedGaitSamples();
		gaitSample = {id:0, description:'Gait sample one', date: new Date(), patient:1};
	}));
	
	it ('Must add a sample gait', function(){
		$httpBackend.whenPOST(webapi.url + 'gait_samples/').respond(function(){
			var id = mockedGaitSamples.addGaitSample(gaitSample);
			return [201, gaitSample, {}];	
		});
		gaitSamplesFacade.addGaitSample(gaitSample).success(function(data, status){
			expect(data).toEqual(gaitSample);
			expect(status).toEqual(201);
		});
		$httpBackend.flush();
	});
	
	it('Must save a gait', function(){
		$httpBackend.whenPUT(webapi.url + 'gait_samples/0/').respond(function (mehtod, url, data, headers){
			mockedGaitSamples.updateSample(0, angular.fromJson(data));
			return [204, "", {}];
		});
		gaitSample.description = 'new description';
		gaitSamplesFacade.updateGaitSample(gaitSample);
		$httpBackend.flush();
		expect(mockedGaitSamples.get(0).description).toEqual('new description');
		
	});

});
