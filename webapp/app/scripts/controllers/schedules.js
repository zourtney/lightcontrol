/*global _ */
'use strict';


//
// Add / edit schedule modal controller
//
var ScheduleEditModalCtrl = function($scope, $modalInstance, method, schedule, Schedule) {
  $scope.originalName = schedule.name;
  $scope.schedule = schedule;

  $scope.outletOptions = [
    { name: 'No change', value: null },
    { name: 'On', value: 0 },
    { name: 'Off', value: 1 }
  ];

  $scope.schedule.outlets = _.map($scope.schedule.outlets, function(outlet) {
    outlet.selectValue = _.findWhere($scope.outletOptions, { value: outlet.value });
    return outlet;
  });

  $scope.ok = function() {
    // Set values based on dropdowns.
    _.each($scope.schedule.outlets, function(outlet) {
      outlet.value = outlet.selectValue.value;
    });

    // Try to save...
    schedule.originalName = $scope.originalName;
    new Schedule(schedule)['$' + method]().then(function(resp) {
      $scope.schedule = resp.data;
      $modalInstance.close($scope.schedule);
    });
  };

  $scope.cancel = function() {
    $modalInstance.dismiss('cancel');
  };
};


//
// Delete schedule modal controller
//
var ScheduleDeleteModalCtrl = function($scope, $modalInstance, schedule, Schedule) {
  $scope.schedule = schedule;

  $scope.ok = function() {
    schedule.originalName = schedule.name;
    new Schedule(schedule).$delete().then(function(data) {
      $scope.schedule = data;
      $modalInstance.close($scope.schedule);
    });
  };

  $scope.cancel = function() {
    $modalInstance.dismiss('cancel');
  };
};


//
// Schedules page controller
//
angular.module('webappApp')
  .controller('SchedulesCtrl', function($scope, Outlets, Schedules, Schedule, $modal) {
    // Load schedules into array at startup
    $scope.schedules = Schedules.query();

    $scope.add = function() {
      var modalInstance,
          schedule = {};

      Outlets.query(function(data) {
        // Create blank schedule, with outlets preset to 'no change'.
        schedule = {
          outlets: _.map(data, function(o) {
            o.value = null;
            return o;
          })
        };

        // Create the modal
        modalInstance = $modal.open({
          templateUrl: 'views/schedule_modal.html',
          controller: ScheduleEditModalCtrl,
          resolve: {
            method: function() {
              return 'save';
            },
            schedule: function() {
              return schedule;
            },
            Schedule: function() {
              return Schedule;
            }
          }
        });

        // Add to `$scope.schedules` on successful save.
        modalInstance.result.then(function(schedule) {
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
        controller: ScheduleEditModalCtrl,
        resolve: {
          method: function() {
            return 'update';
          },
          schedule: function() {
            return angular.copy(self.schedule);
          },
          Schedule: function() {
            return Schedule;
          }
        }
      });

      // Save to server, using PUT
      //NOTE: setting 'originalName' so we PUT to the same URL. Consider switiching to numeric ID system for UIDs.
      modalInstance.result.then(function(schedule) {
        self.schedule = schedule;
      });
    };

    $scope.delete = function() {
      var self = this,
          modalInstance;

      modalInstance = $modal.open({
        templateUrl: 'views/schedule_delete_modal.html',
        controller: ScheduleDeleteModalCtrl,
        resolve: {
          schedule: function() {
            return angular.copy(self.schedule);
          },
          Schedule: function() {
            return Schedule;
          }
        }
      });

      modalInstance.result.then(function(schedule) {
        // Remove from `$scope.schedules`.
        var i = $scope.schedules.indexOf(_.findWhere($scope.schedules, { name: schedule.name }));
        if (i >= 0) {
          $scope.schedules.splice(i, 1);
        }
      });
    };
  });