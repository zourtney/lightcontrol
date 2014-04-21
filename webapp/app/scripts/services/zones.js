'use strict';

angular.module('webappApp').factory('Zones', ['$http', '$q',
  function($http, $q) {
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
  }
]);