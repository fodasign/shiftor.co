ineedtodo = angular.module("ineedtodo", ["ngResource"]);

ineedtodo.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol("{[{");
  $interpolateProvider.endSymbol("}]}");
});