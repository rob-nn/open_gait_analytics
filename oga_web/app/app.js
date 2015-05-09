'use strict';

// Declare app level module which depends on views, and components
angular.module('oga_web', [
	'ngRoute',
	"ngMaterial", 
	"ngMdIcons", 
	'oga_web.gait_analysis', 
	'oga_web.patients',
	'oga_web.patient',
	'oga_web.oga_facade',
	'myApp.view1',
	'myApp.view2',
	'myApp.version',
])
.config(['$routeProvider', function($routeProvider) {
	$routeProvider.otherwise({redirectTo: '/patients'});
}])
.run(function($rootScope) {
	$rootScope.apptitle = 'Open Gait Analytics';
});
