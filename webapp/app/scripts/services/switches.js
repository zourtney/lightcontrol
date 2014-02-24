/*global _ */
'use strict';

var switchesServices = angular.module('switchesServices', ['ngResource']);


switchesServices.factory('Switches', ['$resource', '$http',
  function($resource, $http) {
    var Switches = $resource('/api/switches/');
    angular.extend(Switches.prototype, {
      '$update': function() {
        return $http.put('/api/switches/', _.toArray(this));   // annoying: http://stackoverflow.com/a/14536416/311207
      }
    });
    return Switches;
  }
]);


switchesServices.factory('Switch', ['$resource', function($resource) {
  return $resource('/api/switches/:name', {name: '@name'}, {
    update: { method: 'PUT' }
  });
}]);