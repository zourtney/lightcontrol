'use strict';

angular.module('webappApp', [
  'ngResource',
  'ngCookies',
  'ngSanitize',
  'ngRoute',
  'ui.bootstrap',
  
  'aboutServices'
  // 'schedulesServices',
  // 'switchesServices',
  // 'zonesServices'
]).config(function ($routeProvider) {
  $routeProvider
    .when('/', {
      templateUrl: 'views/home.html',
      controller: 'HomeCtrl'
    })
    .when('/about', {
      templateUrl: 'views/about.html',
      controller: 'AboutCtrl'
    })
    .otherwise({
      redirectTo: '/'
    });
});
