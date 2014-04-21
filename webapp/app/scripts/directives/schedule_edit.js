'use strict';

angular.module('webappApp').directive('lcScheduleEdit', function() {
  return {
    restrict: 'E',
    templateUrl: 'views/schedule_edit.html',
    scope: {
      schedule: '='
    }
  };
});

