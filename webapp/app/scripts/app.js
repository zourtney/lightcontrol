'use strict';

angular.module('webappApp', [
  'ngResource',
  'ngCookies',
  'ngSanitize',
  'ngRoute',
  'ui.bootstrap',
  'outletServices',
  'schedulesServices',
  'aboutServices'
])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/outlets', {
        templateUrl: 'views/outlets.html',
        controller: 'OutletsCtrl'
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
        redirectTo: '/outlets'
      });
  });