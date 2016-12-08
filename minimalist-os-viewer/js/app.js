var treemapDirective = new window.Babbage.TreemapDirective();

var app = angular.module('MinimalistOS', []);

treemapDirective.init(app);

app.controller('treeMapCtrl', function($scope) {
  $scope.cube = '5df4a7b06a940c992d1c44525daff47b:mexican_federal_budget_basis_for_discussion';
  $scope.apiUrl = 'http://next.openspending.org/api/3';
  $scope.stateForCharts = {
    group: ['activity_ID_Modalidad.ID_Modalidad'],
    aggregates: 'Pagado.sum'
  };

  $scope.$on('babbage-ui.click', function($event, component, item) {
    console.log('Click', component, item);
  });
})