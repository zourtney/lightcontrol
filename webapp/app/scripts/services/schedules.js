'use strict';

angular.module('webappApp').factory('Schedules', ['$http', '$q', function($http, $q) {
  return {
    query: function(zone) {
      var deferred = $q.defer(),
          url = zone.isLocal ? '/api/schedules/' : '/api/zones/' + zone.name + '/schedules/';

      $http.get(url)
        .success(function(data) {
          deferred.resolve(data);
        });

      return deferred.promise;
    }
  };
}]);

/*var schedulesServices = angular.module('schedulesServices', ['ngResource']);


schedulesServices.factory('Schedules', ['$resource',
  function($resource) {
    return $resource('/api/schedules/');
  }
]);


schedulesServices.factory('Schedule', ['$resource', '$http', function($resource, $http) {
  var Schedule = $resource('/api/schedules/:originalName', {originalName: '@originalName'}, {
    update: { method: 'PUT' }
  });
  angular.extend(Schedule.prototype, {
    '$save': function() {
      return $http.post('/api/schedules/', this);   // still annoying: http://stackoverflow.com/a/14536416/311207
    }
  });
  return Schedule;
}]);*/