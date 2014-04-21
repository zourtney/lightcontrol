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

    /*$scope.addSchedule = function() {
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
          },
          schedules: function() {
            return $scope.schedules;
          }
        }
      });
    };*/

    $scope.editSchedule = function(schedule) {
      // Create blank schedule, with switches preset to 'no change'.
      if (! schedule) {
        schedule = {
          switches: _.map($scope.switches, function(o) {
            o.value = null;
            return o;
          })
        };
      }

      $modal.open({
        templateUrl: 'views/schedule_edit.html',
        controller: 'ScheduleEditCtrl',
        resolve: {
          schedule: function() {
            return schedule;
          },
          schedules: function() {
            return $scope.schedules;
          }
        }
      });
    };
  }
]);