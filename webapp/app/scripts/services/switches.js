/*global _ */
'use strict';

angular.module('webappApp')
  .factory('Switches', ['$http', '$q', function($http, $q) {

    function copyArrayWithZone(switches, zone) {
      var ret = angular.copy(switches);
      angular.forEach(ret, function(s) {
        s.zone = zone;
      });
      return ret;
    }

    function updateSwitch(swtch, data) {
      angular.forEach(data, function(val, key) {
        if (key && key[0] !== '$') {
          swtch[key] = val;
        }
      });
      return swtch;
    }

    function updateSwitches(switches, data) {
      angular.forEach(switches, function(swtch) {
        // Find data array. It ought to exist...or else there be gremlins.
        var newSwtch = _.findWhere(data, {name: swtch.name});
        updateSwitch(swtch, newSwtch);
      });
    }

    return {
      query: function(zone) {
        var deferred = $q.defer(),
            url = zone.isLocal ? '/api/switches/' : '/api/zones/' + zone.name + '/switches/';

        $http.get(url)
          .success(function(data) {
            deferred.resolve(copyArrayWithZone(data, zone));
          });

        return deferred.promise;
      },
      setOne: function(swtch, val) {
        var deferred = $q.defer(),
            newSwtch = angular.copy(swtch),
            zone = swtch.zone,
            url = zone.isLocal ? '/api/switches/' + swtch.name : '/api/zones/' + zone.name + '/switches/' + swtch.name;

        newSwtch.value = val;

        $http.put(url, newSwtch)
          .success(function(data) {
            deferred.resolve(updateSwitch(swtch, data));
          });

        return deferred.promise;
      },
      setAll: function(switches, val) {
        var deferred = $q.defer(),
            zone = switches[0].zone,
            url = zone.isLocal ? '/api/switches/' : '/api/zones/' + zone.name + '/switches/';

        angular.forEach(switches, function(s) {
          s.value = val;
        });

        $http.put(url, switches)
          .success(function(data) {
            deferred.resolve(updateSwitches(switches, data));
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