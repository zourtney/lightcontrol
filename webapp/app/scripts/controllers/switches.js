'use strict';

angular.module('webappApp')
  .controller('SwitchesCtrl', function($scope, Switches, Switch) {
    // Load switches into array at startup
    $scope.switches = Switches.query();
    
    // Save toggled switch state to server
    $scope.toggleSwitch = function() {
      var self = this,
          s;

      s = new Switch(angular.extend({}, self.switch, {
        value: self.switch.value === 0 ? 1 : 0
      }));

      s.$update().then(function() {
        self.switch = s;
      });
    };

    function setAllSwitches(val) {
      var all = [];
      angular.forEach($scope.switches, function(s) {
        this.push(angular.extend({}, s, {value: val}));
      }, all);

      var switches = new Switches(all);
      switches.$update().then(function(resp) {
        $scope.switches = resp.data;
      });
    }

    $scope.turnAllSwitchesOn = function() {
      setAllSwitches(0);
    };
    $scope.turnAllSwitchesOff = function() {
      setAllSwitches(1);
    };
  });