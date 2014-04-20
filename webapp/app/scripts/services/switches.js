'use strict';

angular.module('webappApp').factory('Switches', ['$http', '$q', function($http, $q) {
  return {
    query: function(zone) {
      var deferred = $q.defer(),
          url = zone.isLocal ? '/api/switches/' : '/api/zones/' + zone.name + '/switches/';

      $http.get(url)
        .success(function(data) {
          deferred.resolve(data);
        });

      return deferred.promise;
    }
  };
}]);


/*switchesServices.factory('Switches', ['$resource', '$http',
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
}]);*/