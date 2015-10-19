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


	var _plotAngles = function (idPositionalsData, angleIndex) {
		return $http.get(urlApi.urlString() + 'gait_sample/' + idPositionalsData + '/' + angleIndex + '/angles/');
	}

	var _plotAngularVelocities = function (idPositionalsData, angleIndex) {
		return $http.get(urlApi.urlString() + 'gait_sample/' + idPositionalsData + '/' + angleIndex + '/angular_velocity/');
	}

	var _plotAngularAccelerations = function (idPositionalsData, angleIndex) {
		return $http.get(urlApi.urlString() + 'gait_sample/' + idPositionalsData + '/' + angleIndex + '/angular_accelerations/');
	}


	var _plotMarker = function (idPositionalsMarkers,  marker) {
		return $http.get(urlApi.urlString() + 'gait_sample/' + idPositionalsMarkers + '/' + marker + '/');
	};

	var _deletePositionalsData = function (idPos) {
		return $http.delete(urlApi.urlString() + 'gait_sample/positionals_data/' + idPos + '/');
	};

	var _getTrajectories = function (idPos) {
		return $http.get(urlApi.urlString() + 'gait_sample/positional_data/'+ idPos +'/trajectories/');
	}
	return {
		getPositionalsData : _getPositionalsData, 
		getTrajectories : _getTrajectories, 
		updatePositionalsData : _updatePositionalsData, 
		plotAngles : _plotAngles,
		plotAngularVelocities : _plotAngularVelocities, 
		plotAngularAccelerations: _plotAngularAccelerations,
		plotMarker : _plotMarker,
		deletePositionalsData : _deletePositionalsData
	};
}).factory('simulationFacade', function($http, urlApi){
	var _runCmacTraing = function (idPatient, idGaitSample, activationsNumber, iterationsNumber, output, markers, angles) {
		var cmacConfig =  {
			idPatient: idPatient, 
			idGaitSample: idGaitSample, 
			activationsNumber: activationsNumber, 
			iterationsNumber: iterationsNumber, 
			output: output, 
			markers: markers, 
			angles: angles
		};
		return $http.post(urlApi.urlString() + 'simulation/cmac/training/', cmacConfig);
	};
	return {
		runCmacTraining: _runCmacTraing
	};
});
