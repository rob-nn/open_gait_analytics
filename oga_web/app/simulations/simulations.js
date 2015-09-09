'use strict';
angular.module('oga_web.simulations', ["ngRoute", "ngMaterial", "ngMdIcons"])
.config(['$routeProvider', function($routeProvider) {
	$routeProvider
	.when("/simulations", {
		templateUrl: "simulations/simulations.html",
		controller: "simulationsCtrl" 
	});
}])
.controller('simulationsCtrl', function ($scope, $location){
	$scope.goBack = goBack;
	function goBack() {
		$location.path("/");
	};
});
