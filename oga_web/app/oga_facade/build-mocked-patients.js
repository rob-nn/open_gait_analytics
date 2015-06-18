buildMockedPatients = function () {
	var _patients =[
		{ 
			_id: {$oid: 0},
			name: 'Roberto A. Lima',
			birth: new Date(1977, 11, 19)
		},
		{
			_id: {$oid: 1},
			name: 'Joseph Smith',
			birth: new Date(1980, 1, 1)
		}
	];
	var _getPatient = function (id) {return _patients[id];};
	var _getPatients = function () {return _patients;};
	var _addPatient = function(patient) {
		patient._id = _patients.length;
		return  _patients.push(patient)
	};

	return {
		getPatients : _getPatients,
		getPatient : _getPatient, 
		addPatient : _addPatient
	}
};

