'use strict';

angular.module('webappApp').directive('lcSwitchList', function() {
  return {
    restrict: 'E',
    templateUrl: 'views/switch_list.html',
    scope: {
      switches: '=',
      toggleSwitch: '=',
      setSwitches: '='
    }
  };
});