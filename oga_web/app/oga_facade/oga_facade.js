'use strict';
angular.module('oga_web.oga_facade', [])
.factory('urlApi', function($http, $location) {
	return {'urlString': function() {return 'http://' + $location.host() + ':5000/api/v0.0/'}};	
})
.factory('gaitSamplesFacade', function($http, urlApi) {
	var _addGaitSample = function(sample){
		return $http.post(urlApi.urlString() + 'gait_samples/', sample);
	}

	return {
		addGaitSample: _addGaitSample,
	};
})
.factory('patientsFacade', function($http, urlApi){
	var _getPatient = function(id) {
		return $http.get(urlApi.urlString() + 'patients/' + id + '/');
	}
	var _getPatients = function() {
		return $http.get(urlApi.urlString() + 'patients/');
	};
	var _addPatient = function(patient) {
		return $http.post(urlApi.urlString() + 'patients/', patient);
	};

	var _updatePatient = function(patient) {
		return $http.put(urlApi.urlString() + 'patients/', patient);
	};
	return {
		getPatients: _getPatients,
		getPatient: _getPatient,
		addPatient: _addPatient,
		updatePatient: _updatePatient
	};
});
