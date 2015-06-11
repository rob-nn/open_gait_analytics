'use strict';
angular.module('oga_web.oga_facade', [])
.factory('urlApi', function($http, $location) {
	return {'urlString': function() {return 'http://' + $location.host() + ':5000/api/v0.0/'}};	
})
.factory('gaitSamplesFacade', function($http, urlApi) {
	var _addGaitSample = function(sample){
		return $http.post(urlApi.urlString() + 'gait_samples/', sample);
	}
	var _updateGaitSample = function(sample) {
		return $http.put(urlApi.urlString() + 'gait_samples/' + sample.id + '/', sample);
	}

	return {
		addGaitSample: _addGaitSample,
		updateGaitSample: _updateGaitSample
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
	return {
		getPatients: _getPatients,
		getPatient: _getPatient,
		addPatient: _addPatient
	};
});
