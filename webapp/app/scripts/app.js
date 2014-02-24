'use strict';

angular.module('webappApp', [
  'ngResource',
  'ngCookies',
  'ngSanitize',
  'ngRoute',
  'ui.bootstrap',
  'switchesServices',
  'schedulesServices',
  'aboutServices'
])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/switches', {
        templateUrl: 'views/switches.html',
        controller: 'SwitchesCtrl'
      })
      .when('/schedules', {
        templateUrl: 'views/schedules.html',
        controller: 'SchedulesCtrl'
      })
      .when('/about', {
        templateUrl: 'views/about.html',
        controller: 'AboutCtrl'
      })
      .otherwise({
        redirectTo: '/switches'
      });
  });