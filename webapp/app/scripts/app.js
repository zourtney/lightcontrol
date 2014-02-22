'use strict';

angular.module('webappApp', [
  'ngResource',
  'ngCookies',
  'ngSanitize',
  'ngRoute',
  'outletServices',
  'schedulesServices'
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
      .otherwise({
        redirectTo: '/outlets'
      });
  });