'use strict';
angular.module('oga_web.oga_facade', [])
.factory('urlApi', function($http, $location) {
	return {'urlString': function() {return 'http://' + $location.host() + ':5000/api/v0.0/'}};	
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
		return $http.put(urlApi.urlString() + 'patients/',  patient);
	};

	var _showGraph = function(){
		return $http.get(urlApi.urlString() + 'concept/graph');
	}

	return {
		getPatients: _getPatients,
		getPatient: _getPatient,
		addPatient: _addPatient,
		updatePatient: _updatePatient,
		showGraph: _showGraph 
	};
})
.factory('positionalsDataFacade', function($http, urlApi){
	var _getPositionalsData = function (idPatient, gaitSampleIndex) {
		return $http.get(urlApi.urlString() + 'gait_sample/positional_data/' + idPatient + '/' + gaitSampleIndex + '/');
	};

	var _updatePositionalsData = function (positionalsData) {
		return $http.put(urlApi.urlString() + 'gait_sample/positionals_data/', positionalsData);
	};

	var _plotMarker = function (idPositionalsMarkers,  marker) {
		return $http.get(urlApi.urlString() + 'gait_sample/' + idPositionalsMarkers + '/' + marker + '/');
	}


	return {
		getPositionalsData : _getPositionalsData, 
		updatePositionalsData : _updatePositionalsData, 
		plotMarker: _plotMarker
	};
});

