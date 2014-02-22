'use strict';


// Please note that $modalInstance represents a modal window (instance) dependency.
// It is not the same as the $modal service used above.

var ModalInstanceCtrl = function ($scope, $modalInstance, schedule, Outlets) {
  $scope.schedule = schedule;

  var allOutlets = Outlets.query(function(data) {
    $scope.mergedOutlets = _.map(data, function(outlet) {
      return _.extend({}, outlet, {
        value: 1
      });
    });
  });

  /*$scope.ok = function () {
    $modalInstance.close($scope.selected.item);
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };*/
};



angular.module('webappApp')
  .controller('SchedulesCtrl', function($scope, Schedules, $modal) {
    // Load schedules into array at startup
    $scope.schedules = Schedules.query();

    $scope.open = function() {
      var self = this,
          modalInstance;

      modalInstance = $modal.open({
        templateUrl: 'views/schedule_modal.html',
        controller: ModalInstanceCtrl,
        resolve: {

          schedule: function() {
            return self.schedule;
          }
        }
      });

      modalInstance.result.then(function (selectedItem) {
        $scope.selected = selectedItem;
      });
    };
  });