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


