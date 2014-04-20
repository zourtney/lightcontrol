'use strict';

angular.module('webappApp').directive('lcScheduleList', function() {
  return {
    restrict: 'E',
    templateUrl: 'views/schedule_list.html',
    scope: {
      schedules: '='
    }
  };
});

