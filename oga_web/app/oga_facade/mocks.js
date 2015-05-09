buildMockedPatients = function () {
	var _patients =[
		{ 
			name: 'Roberto A. Lima',
			birth: new Date(1977, 11, 19)
		},
		{
			name: 'Joseph Smith',
			birth: new Date(1980, 1, 1)
		}
	];
	var _id = function(id) {return id -1;};
	var _getPatient = function (id) {return _patients[_id(id)];};
	var _getPatients = function () {return _patients;};
	var _addPatient = function(patient) {
		return _patients.push(patient);
	};

	return {
		getPatients : _getPatients,
		getPatient : _getPatient, 
		addPatient : _addPatient
	}
};

buildMockedGaitSamples = function () {
	var _gaitSamples = [];

	var _addGaitSample = function(gaitSample) {
		return _gaitSamples.push(gaitSample) - 1;
	}

	var _updateGaitSample = function(id, gaitSample) {
		_gaitSamples[id] = gaitSample;					
	}
	var _get = function (id){
		return _gaitSamples[id];
	}

	return {
		gaitSamples : _gaitSamples,
		addGaitSample : _addGaitSample,
		updateSample : _updateGaitSample,
		get: _get
	};
};
