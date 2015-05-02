oga.config(function($routeProvider){

	$routeProvider
	.when("/patients", {
		templateUrl: "patients.html",
		controller: "patientsCtrl", 
		resolve: {
			patients: function(ogaFacade) {
				return ogaFacade.getPatients();
			}
		}
	})
	.when("/patients_new", {
		templateUrl: "patient.html",
		controller: "patientNewCtrl",
	})
/*	.when("/patient/:id", {
		templateUrl: "patient.html",
		controller: "patientCtrl",
		resolve: {
			"patient": function(ogaFacade, $route) {
				var id = $route.current.params.id;
				return ogaFacade.getPaptient(id);
			}
		}
	})*/
	.otherwise({
		redirectTo: '/patients'
	});
});

oga.constant("ogawebapiConstant", {
	url:  'http://localhost:8000/patients/'
});
