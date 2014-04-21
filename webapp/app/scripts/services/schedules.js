'use strict';

angular.module('webappApp').factory('Schedules', ['$http', '$q',
  function($http, $q) {

    function copyArrayWithZone(schedules, zone) {
      var ret = angular.copy(schedules);
      angular.forEach(ret, function(s) {
        s.zone = zone;
      });
      return ret;
    }
    
    function updateSchedule(schedule, data) {
      angular.forEach(data, function(val, key) {
        if (key && key[0] !== '$') {
          schedule[key] = val;
        }
      });
      return schedule;
    }

    function getUrlPrefix(zone) {
      return zone.isLocal ? '/api/schedules' : '/api/zones/' + zone.name + '/schedules';
    }

    return {
      query: function(zone) {
        var deferred = $q.defer(),
            url = zone.isLocal ? '/api/schedules/' : '/api/zones/' + zone.name + '/schedules/';

        $http.get(url)
          .success(function(data) {
            deferred.resolve(copyArrayWithZone(data, zone));
          });

        return deferred.promise;
      },
      setOne: function(schedule) {
        var deferred = $q.defer(),
            url = getUrlPrefix(schedule.zone) + '/' + schedule.originalName;

        $http.put(url, schedule)
          .success(function(data) {
            deferred.resolve(updateSchedule(schedule, data));
          });

        return deferred.promise;
      },
      addOne: function(schedule) {
        var deferred = $q.defer(),
            url = getUrlPrefix(schedule.zone) + '/';

        $http.post(url, schedule)
          .success(function(data) {
            deferred.resolve(updateSchedule(schedule, data));
          });

        return deferred.promise;
      },
      deleteOne: function(schedule) {
        var deferred = $q.defer(),
            url = getUrlPrefix(schedule.zone) + '/' + schedule.name;

        $http.delete(url, schedule)
          .success(function(data) {
            deferred.resolve(updateSchedule(schedule, data));
          });

        return deferred.promise;
      }
    };
  }
]);