angular.module("uploadModule", ["ngMaterial", "lfNgMdFileInput"], function($interpolateProvider) {
    $interpolateProvider.startSymbol("[[");
    $interpolateProvider.endSymbol("]]");
});