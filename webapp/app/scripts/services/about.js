'use strict';

angular.module('webappApp').factory('Version', ['$resource',
  function($resource) {
    return $resource('/api/version');
  }
]);