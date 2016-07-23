angular.module("uploadModule")
    .controller("filesController", [
        "$http", function($http) {
            var ctrl = this;
            ctrl.updateFiles = function() {
                $http.get("/api/files").then(function(response){
                    ctrl.files = response.data;
                });
            };
            ctrl.updateFiles();

            ctrl.download = function(urlArray, filename) {
                url = urlArray[0][0];
                window.open(url, "_blank");
            }
        }
    ]);