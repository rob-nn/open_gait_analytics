oga.factory("ogaFacade", function($http, ogawebapiConstant){
	var _getPatient = function(id) {
		return $http.get(ogawebapiConstant.url + id + '/');
	}
	var _getPatients = function() {
		return $http.get(ogawebapiConstant.url);
	};
	var _addPatient = function(patient) {
		return $http.post(ogawebapiConstant.url, patient);
	};
	return {
		getPatients: _getPatients,
		getPatient: _getPatient,
		addPatient: _addPatient
	};
});



