'use strict';

angular.module('webappApp').directive('lcZoneSelect', function() {
  return {
    restrict: 'E',
    templateUrl: 'views/zone_select.html',
    scope: {
      zones: '=',
      currentZone: '='
    }
  };
});