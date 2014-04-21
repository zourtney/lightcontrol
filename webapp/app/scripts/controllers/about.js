'use strict';

angular.module('webappApp').controller('AboutCtrl', ['$scope', '$modalInstance', 'Version',
  function($scope, $modalInstance, Version) {
    $scope.version = Version.get();

    $scope.close = function() {
      $modalInstance.dismiss('cancel');
    };
  }
]);