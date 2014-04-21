'use strict';

angular.module('webappApp').controller('HomeCtrl', ['$scope', 'Zones', 'Switches', 'Schedules',
  function($scope, Zones, Switches, Schedules) {
    // Get available zones
    Zones.query().then(function(data) {
      $scope.zones = data;
      $scope.currentZone = $scope.zones[0];
    });

    function getSwitches() {
      Switches.query($scope.currentZone).then(function(data) {
        $scope.switches = data;
      });
    }

    function getSchedules() {
      Schedules.query($scope.currentZone).then(function(data) {
        $scope.schedules = data;
      });
    }

    // Update switches and schedules on zone change
    $scope.$watch('currentZone', function() {
      if ($scope.currentZone) {
        getSwitches();
        getSchedules();
      }
    });

    $scope.toggleSwitch = function(swtch) {
      Switches.setOne(swtch, swtch.value === 0 ? 1 : 0);
    };

    $scope.setSwitches = function(val) {
      Switches.setAll($scope.switches, val);
    };
  }
]);