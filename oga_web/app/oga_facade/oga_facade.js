'use strict';
angular.module('oga_web.oga_facade', [])
.constant("webapi", {
	url:  'http://localhost:5000/api/v0.0/'
})
.factory('gaitSamplesFacade', function($http, webapi) {
	var _addGaitSample = function(sample){
		return $http.post(webapi.url + 'gait_samples/', sample);
	}
	var _updateGaitSample = function(sample) {
		return $http.put(webapi.url + 'gait_samples/' + sample.id + '/', sample);
	}

	return {
		addGaitSample: _addGaitSample,
		updateGaitSample: _updateGaitSample
	};
})
.factory('patientsFacade', function($http, webapi){
	var _getPatient = function(id) {
		return $http.get(webapi.url + 'patients/' + id + '/');
	}
	var _getPatients = function() {
		return $http.get(webapi.url + 'patients/');
	};
	var _addPatient = function(patient) {
		return $http.post(webapi.url + 'patients/', patient);
	};
	return {
		getPatients: _getPatients,
		getPatient: _getPatient,
		addPatient: _addPatient
	};
});
