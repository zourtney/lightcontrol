'use strict';

angular.module('webappApp').directive('lcZoneBanner', function() {
  return {
    restrict: 'E',
    templateUrl: 'views/zone_banner.html',
    scope: {
      currentZone: '='
    }
  };
});