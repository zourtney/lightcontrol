/*global _ */
'use strict';

angular.module('webappApp').controller('ScheduleEditCtrl', ['$scope', '$modalInstance', 'schedule', 'schedules', 'Schedules',
  function($scope, $modalInstance, schedule, schedules, Schedules) {
    $scope.original = schedule;
    $scope.schedule = angular.copy(schedule);

    $scope.switchOptions = [
      { name: 'No change', value: null },
      { name: 'On', value: 0 },
      { name: 'Off', value: 1 }
    ];

    // Add 'selectedValue' property
    $scope.schedule.switches = _.map($scope.schedule.switches, function(s) {
      s.selectValue = _.findWhere($scope.switchOptions, { value: s.value });
      return s;
    });

    function updateSchedule(sched, data) {
      angular.forEach(data, function(val, key) {
        if (key && key[0] !== '$') {
          sched[key] = val;
        }
      });
      return sched;
    }

    $scope.cancel = function() {
      $modalInstance.dismiss('cancel');
    };

    $scope.ok = function() {
      $scope.schedule.originalName = $scope.original.name;
      
      _.each($scope.schedule.switches, function(s) {
        s.value = s.selectValue.value;
      });

      if ($scope.original.name) {
        // Update existing model
        Schedules.setOne($scope.schedule).then(function(data) {
          updateSchedule($scope.original, data);
          $modalInstance.close($scope.original);
        });
      }
      else {
        // Create a new one
        Schedules.addOne($scope.schedule).then(function(data) {
          updateSchedule($scope.original, data);
          schedules.push($scope.original);
          $modalInstance.close($scope.original);
        });
      }
    };

    $scope.delete = function() {
      Schedules.deleteOne($scope.original).then(function(data) {
        // Remove from 'schedules' array.
        var i = schedules.indexOf(_.findWhere(schedules, { name: data.name }));
        if (i >= 0) {
          schedules.splice(i, 1);
        }
        $modalInstance.close();
      });
    };
  }
]);