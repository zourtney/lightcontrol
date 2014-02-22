'use strict';

angular.module('webappApp')
  .controller('AboutCtrl', function($scope, Version) {
    $scope.version = Version.get();
  });