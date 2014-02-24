'use strict';

angular.module('webappApp')
  .controller('AboutCtrl', ['$scope', 'Version',
    function($scope, Version) {
      $scope.version = Version.get();
    }
  ]);