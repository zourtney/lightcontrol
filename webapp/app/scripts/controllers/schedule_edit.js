/*global _ */
'use strict';

var webAppModule = angular.module('webappApp');



//
// Add / edit schedule modal controller
//
webAppModule.controller('ScheduleEditCtrl', ['$scope', '$modalInstance', 'schedule', 'schedules', 'Schedules',
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

/*
//
// Delete schedule modal controller
//
webAppModule.controller('ScheduleDeleteModalCtrl', ['$scope', '$modalInstance', 'schedule',
  function($scope, $modalInstance, schedule) {
    $scope.schedule = schedule;

    $scope.ok = function() {
      $modalInstance.close($scope.schedule);
    };

    $scope.cancel = function() {
      $modalInstance.dismiss('cancel');
    };
  }
]);


//
// Schedules page controller
//
webAppModule.controller('SchedulesCtrl', ['$scope', 'Switches', 'Schedules', 'Schedule', '$modal',
  function($scope, Switches, Schedules, Schedule, $modal) {
    // Load schedules into array at startup
    $scope.schedules = Schedules.query();

    $scope.add = function() {
      var modalInstance,
          schedule = {};

      Switches.query(function(data) {
        // Create blank schedule, with switches preset to 'no change'.
        schedule = {
          switches: _.map(data, function(o) {
            o.value = null;
            return o;
          })
        };

        // Create the modal
        modalInstance = $modal.open({
          templateUrl: 'views/schedule_modal.html',
          controller: 'ScheduleEditModalCtrl',
          resolve: {
            schedule: function() {
              return schedule;
            }
          }
        });

        // Add to `$scope.schedules` on successful save.
        modalInstance.result.then(function(schedule) {
          schedule.originalName = schedule.name;
          new Schedule(schedule).$save().then(function(resp) {
            $scope.schedules.push(resp.data);
          });
        });
      });
    };

    $scope.open = function() {
      var self = this,
          modalInstance;

      modalInstance = $modal.open({
        templateUrl: 'views/schedule_modal.html',
        controller: 'ScheduleEditModalCtrl',
        resolve: {
          schedule: function() {
            return angular.copy(self.schedule);
          }
        }
      });

      // Save to server, using PUT
      //NOTE: setting 'originalName' so we PUT to the same URL. Consider switiching to numeric ID system for UIDs.
      modalInstance.result.then(function(schedule) {
        schedule.originalName = self.schedule.name;
        new Schedule(schedule).$update().then(function(data) {
          self.schedule = data;
        });
      });
    };

    $scope.delete = function() {
      var self = this,
          modalInstance;

      modalInstance = $modal.open({
        templateUrl: 'views/schedule_delete_modal.html',
        controller: 'ScheduleDeleteModalCtrl',
        resolve: {
          schedule: function() {
            return angular.copy(self.schedule);
          }
        }
      });

      modalInstance.result.then(function(schedule) {
        schedule.originalName = schedule.name;
        new Schedule(schedule).$delete().then(function() {
          // Remove from `$scope.schedules`.
          var i = $scope.schedules.indexOf(_.findWhere($scope.schedules, { name: schedule.name }));
          if (i >= 0) {
            $scope.schedules.splice(i, 1);
          }
        });
      });
    };
  }
]);*/