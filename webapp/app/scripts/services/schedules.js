'use strict';

var schedulesServices = angular.module('schedulesServices', ['ngResource']);


schedulesServices.factory('Schedules', ['$resource',
  function($resource) {
    var Schedules = $resource('/api/schedules/');
    angular.extend(Schedules.prototype, {
      // '$update': function() {
      //   return $http.put('/api/schedules/', _.toArray(this));   // annoying: http://stackoverflow.com/a/14536416/311207
      // }
    });
    return Schedules;
  }
]);


schedulesServices.factory('Schedules', ['$resource', function($resource) {
  return $resource('/api/schedules/:id', {id: '@id'}, {
    update: { method: 'PUT' }
  });
}]);