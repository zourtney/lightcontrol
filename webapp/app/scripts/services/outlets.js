/*global _ */
'use strict';

var outletServices = angular.module('outletServices', ['ngResource']);


outletServices.factory('Outlets', ['$resource', '$http',
  function($resource, $http) {
    var Outlets = $resource('/api/outlets/');
    angular.extend(Outlets.prototype, {
      '$update': function() {
        return $http.put('/api/outlets/', _.toArray(this));   // annoying: http://stackoverflow.com/a/14536416/311207
      }
    });
    return Outlets;
  }
]);


outletServices.factory('Outlet', ['$resource', function($resource) {
  return $resource('/api/outlets/:id', {id: '@id'}, {
    update: { method: 'PUT' }
  });
}]);