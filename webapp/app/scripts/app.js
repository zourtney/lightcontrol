'use strict';

angular.module('webappApp', [
  'ngResource',
  'ngCookies',
  'ngSanitize',
  'ngRoute',
  //'outletServices'
])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl'
      })
      .otherwise({
        redirectTo: '/'
      });
  });