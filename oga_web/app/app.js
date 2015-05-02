'use strict';

// Declare app level module which depends on views, and components
angular.module('oga_web', [
	'ngRoute',
	"ngMaterial", 
	"ngMdIcons", 
	"ui.bootstrap",
	'oga_web.patients',
	'oga_web.patient',
	'myApp.view1',
	'myApp.view2',
	'myApp.version',
])
.config(['$routeProvider', function($routeProvider) {
	$routeProvider.otherwise({redirectTo: '/patients'});
}])
.constant("ogawebapiConstant", {
	url:  'http://localhost:8000/patients/'
})
.run(function($rootScope) {
	$rootScope.apptitle = 'Open Gait Analytics';
});
