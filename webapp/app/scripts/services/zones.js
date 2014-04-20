'use strict';

angular.module('webappApp').factory('Zones', ['$http', '$q', function($http, $q) {
  return {
    query: function() {
      var deferred = $q.defer(),
          url = '/api/zones/';

      $http.get(url)
        .success(function(data) {
          var local = [{name: 'Local', isLocal: true}];
          deferred.resolve(local.concat(data));
        });

      return deferred.promise;
    }
  };
}]);

/*var zonesServices = angular.module('zonesServices', ['ngResource']);


zonesServices.factory('Zones', ['$resource', '$http',
  function($resource, $http) {
    var Zones = $resource('/api/zones/');
    angular.extend(Zones.prototype, {
      '$update': function() {
        return $http.put('/api/zones/', _.toArray(this));   // annoying: http://stackoverflow.com/a/14536416/311207
      }
    });
    return Zones;
  }
]);


zonesServices.factory('Zones', ['$resource', function($resource) {
  return $resource('/api/zones/:name', {name: '@name'}, {
    update: { method: 'PUT' }
  });
}]);*/