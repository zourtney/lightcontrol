/*global _ */
'use strict';


var ScheduleEditModalCtrl = function($scope, $modalInstance, schedule) {
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
    _.each($scope.schedule.outlets, function(outlet) {
      outlet.value = outlet.selectValue.value;
    });
    $modalInstance.close($scope.schedule);
  };

  $scope.cancel = function() {
    $modalInstance.dismiss('cancel');
  };
};


var ScheduleDeleteModalCtrl = function($scope, $modalInstance, schedule) {
  $scope.schedule = schedule;

  $scope.ok = function() {
    $modalInstance.close($scope.schedule);
  };

  $scope.cancel = function() {
    $modalInstance.dismiss('cancel');
  }
};



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
            schedule: function() {
              return schedule;
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
        controller: ScheduleDeleteModalCtrl,
        resolve: {
          schedule: function() {
            return angular.copy(self.schedule);
          }
        }
      });

      // DELETE from server
      //NOTE: same 'originalName' junk as above. It's required (for now) in the angular resource.
      modalInstance.result.then(function(schedule) {
        schedule.originalName = self.schedule.name;
        new Schedule(schedule).$delete().then(function(data) {
          var i = $scope.schedules.indexOf(_.findWhere($scope.schedules, { name: data.name }));
          if (i >= 0) {
            $scope.schedules.splice(i, 1);
          }
        });
      });
    };
  });