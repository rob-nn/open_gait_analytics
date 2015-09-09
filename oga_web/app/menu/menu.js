'use strict';
angular.module('oga_web.menu', ["ngRoute", "ngMaterial", "ngMdIcons"])
.config(['$routeProvider', function($routeProvider) {
	$routeProvider
	.when("/menu", {
		templateUrl: "menu/menu.html",
		controller: "menuCtrl" 
	});
}])
.controller('menuCtrl', function ($scope, $location){
	$scope.goToPatients = goToPatients;
	$scope.goToSimulations = goToSimulations;

	function goToPatients() {
		$location.path("/patients/");
	};

	function goToSimulations() {
		$location.path("/simulations/");
	};
});
