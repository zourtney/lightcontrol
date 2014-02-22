'use strict';

angular.module('webappApp')
  .controller('OutletsCtrl', function($scope, Outlets, Outlet) {
    // Load outlets into array at startup
    $scope.outlets = Outlets.query();
    
    // Save toggled outlet state to server
    $scope.toggleOutlet = function() {
      var self = this,
          outlet;

      outlet = new Outlet(angular.extend({}, self.outlet, {
        value: self.outlet.value === 0 ? 1 : 0
      }));

      outlet.$update().then(function() {
        self.outlet = outlet;
      });
    };

    function setAllOutlets(val) {
      var all = [];
      angular.forEach($scope.outlets, function(outlet) {
        this.push(angular.extend({}, outlet, {value: val}));
      }, all);

      var outlets = new Outlets(all);
      outlets.$update().then(function(resp) {
        $scope.outlets = resp.data;
      });
    }

    $scope.turnAllOutletsOn = function() {
      setAllOutlets(0);
    };
    $scope.turnAllOutletsOff = function() {
      setAllOutlets(1);
    };
  });