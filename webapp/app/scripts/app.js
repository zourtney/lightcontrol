'use strict';

angular.module('webappApp', [
  'ngResource',
  'ngCookies',
  'ngSanitize',
  'ngRoute',
  'ui.bootstrap'
]).config(function ($routeProvider) {
  $routeProvider
    .when('/', {
      templateUrl: 'views/home.html',
      controller: 'HomeCtrl'
    })
    .otherwise({
      redirectTo: '/'
    });
});
