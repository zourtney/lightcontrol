'use strict';

angular.module('webappApp')
  .controller('SchedulesCtrl', function($scope, Schedules) {
    // Load schedules into array at startup
    $scope.schedules = Schedules.query();
  });