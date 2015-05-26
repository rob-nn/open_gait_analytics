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

