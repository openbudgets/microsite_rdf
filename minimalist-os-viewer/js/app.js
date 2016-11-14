var treemapDirective = new window.Babbage.TreemapDirective();

var app = angular.module('MinimalistOS', []);

treemapDirective.init(app);

app.controller('treeMapCtrl', function($scope) {
  $scope.cube = 'boost:boost-moldova-2005-2014';
  $scope.apiUrl = 'http://next.openspending.org/api/3';
  $scope.stateForCharts = {
    group: ['administrative_classification_2.admin1'],
    aggregates: 'adjusted.sum'
  };

  $scope.$on('babbage-ui.click', function($event, component, item) {
    console.log('Click', component, item);
  });
})