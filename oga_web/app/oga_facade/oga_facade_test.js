'use strict'

describe ('Patients Facade specification.',function(){
	var patientsFacade, $httpBackend, mockedPatients, webapi;
	beforeEach(module('oga_web.oga_facade'));
	beforeEach(inject(function(_patientsFacade_, _$httpBackend_, urlApi){
		patientsFacade = _patientsFacade_;
		$httpBackend = _$httpBackend_;
		webapi = urlApi.urlString(); 
		mockedPatients = buildMockedPatients();
	}));

	it ('Must have patients', function(){
		$httpBackend.whenGET(webapi + 'patients/').respond(function(){
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
		$httpBackend.whenGET(webapi + 'patients/' + 1 + '/').respond(function(){
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
		$httpBackend.whenPOST(webapi + 'patients/').respond(function(){
			var id = mockedPatients.addPatient(patient);
			return [201, mockedPatients.getPatient(id -1), {}];	
		});
		patientsFacade.addPatient(patient).success(function(data, status){
			expect(data.name).toEqual(patient.name);
			expect(status).toEqual(201);
		});
		$httpBackend.flush();
	});

	it('Must update a patient', function (){
		var patient = {_id: {$oid: 1} , name : 'Mary', birth:new Date(1984, 12, 1)};
		$httpBackend.whenPUT(webapi + 'patients/').respond(function(method, url, data){
			var d = JSON.parse(data);
			expect(d["_id"]).toEqual(patient._id);
			return [200,  {}, {}]
		});

		patientsFacade.updatePatient(patient).success(function(data, status){
			expect(status).toEqual(200);	
		});
		$httpBackend.flush();
	});
});

describe('PositionalsData especification tests', function(){
	var positionalsDataFacade, $httpBackend, webapi;
	beforeEach(module('oga_web.oga_facade'));
	beforeEach(inject(function(_positionalsDataFacade_, _$httpBackend_, urlApi){
		positionalsDataFacade = _positionalsDataFacade_;
		$httpBackend = _$httpBackend_;
		webapi = urlApi.urlString(); 
	}));

	it ('Must get a positional data', function(){
		$httpBackend.whenGET(webapi + 'gait_sample/positional_data/0/0/').respond(function(){
			var pos = {'_id':0} 
			return [200, pos, {}];
		});
		positionalsDataFacade.getPositionalsData(0, 0).success(function(data, status){
			expect(status).toEqual(200);
			expect(data).toBeDefined();
			expect(data._id).toEqual(0);
		});
		$httpBackend.flush();
	});

	it('Must update positionals data', function (){
		$httpBackend.whenPUT(webapi + 'gait_sample/positionals_data/').respond(function(method, url, data) {
			data = angular.fromJson(data)
			expect(data._id).toBeDefined();
			expect(data._id).toBe(0);
			return [200, {}, {}];
		});
		var pos = {'_id': 0}
		positionalsDataFacade.updatePositionalsData(pos).success(function(data, status){
			expect(status).toEqual(200);
		});
		$httpBackend.flush()
	});

	it('Must delete positionals data', function(){
		$httpBackend.whenDELETE(webapi + 'gait_sample/positionals_data/0/').respond(function(method, url, data){
			return [200, {}, {}];
		});	
		positionalsDataFacade.deletePositionalsData(0).success(function(data, status){
			expect(status).toEqual(200);
		});
		$httpBackend.flush();
	});

	it('Must plot marker', function (){
		$httpBackend.whenGET(webapi + 'gait_sample/1/2/').respond(function(method, url, data){
			return [200, {}, {}]
		});
		positionalsDataFacade.plotMarker(1, 2).success(function(data, status) {
			expect(status).toEqual(200);
		});
		$httpBackend.flush();
	});

});

