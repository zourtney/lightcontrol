/*global _ */
'use strict';

angular.module('webappApp').controller('HomeCtrl', ['$scope', 'Zones', 'Switches', 'Schedules', '$modal',
  function($scope, Zones, Switches, Schedules, $modal) {
    //
    // Zones
    //
    Zones.query().then(function(data) {
      $scope.zones = data;
      $scope.currentZone = $scope.zones[0];
    });

    $scope.$watch('currentZone', function() {
      if ($scope.currentZone) {
        getSwitches();
        getSchedules();
      }
    });


    //
    // Switches
    //
    function getSwitches() {
      Switches.query($scope.currentZone).then(function(data) {
        $scope.switches = data;
      });
    }

    $scope.toggleSwitch = function(swtch) {
      Switches.setOne(swtch, swtch.value === 0 ? 1 : 0);
    };

    $scope.setSwitches = function(val) {
      Switches.setAll($scope.switches, val);
    };


    //
    // Schedules
    //
    function getSchedules() {
      Schedules.query($scope.currentZone).then(function(data) {
        $scope.schedules = data;
      });
    }

    $scope.addSchedule = function() {
      var schedule, modalInstance;

      // Create blank schedule, with switches preset to 'no change'.
      schedule = {
        switches: _.map($scope.switches, function(o) {
          o.value = null;
          return o;
        })
      };

      // Create the modal
      modalInstance = $modal.open({
        templateUrl: 'views/schedule_edit.html',
        controller: 'ScheduleEditCtrl',
        resolve: {
          schedule: function() {
            return schedule;
          }
        }
      });

      // Add to `$scope.schedules` on successful save.
      modalInstance.result.then(function(schedule) {
        schedule.originalName = schedule.name;
        Schedules.addOne(schedule).then(function(data) {
          $scope.schedules.push(data);
        });
      });
    };

    $scope.editSchedule = function(schedule) {
      var modalInstance = $modal.open({
        templateUrl: 'views/schedule_edit.html',
        controller: 'ScheduleEditCtrl',
        resolve: {
          schedule: function() {
            return angular.copy(schedule);
          }
        }
      });

      modalInstance.result.then(function(newSchedule) {
        //NOTE: setting 'originalName' so we PUT to the same URL. Consider switiching to numeric ID system for UIDs.
        newSchedule.originalName = schedule.name;

        // Save to server, then copy back into `schedule`.
        Schedules.setOne(newSchedule).then(function(updatedNewSchedule) {
          angular.forEach(updatedNewSchedule, function(val, key) {
            if (key && key[0] !== '$') {
              schedule[key] = val;
            }
          });
        });
      });
    };
  }
]);