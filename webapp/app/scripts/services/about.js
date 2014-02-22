'use strict';

var aboutServices = angular.module('aboutServices', ['ngResource']);


aboutServices.factory('Version', ['$resource',
  function($resource) {
    return $resource('/api/version');
  }
]);