angular.module("uploadModule")
    .controller("filesController", [
        "$http", "$mdDialog", "$mdMedia", "$scope", function($http, $mdDialog, $mdMedia, $scope) {
            var ctrl = this;
            ctrl.updateFiles = function() {
                $http.get("/api/files").then(function(response){
                    ctrl.files = response.data.files;
                });
            };
            ctrl.updateFiles();

            ctrl.download = function(url) {
                window.open(url, "_blank");
            };

            ctrl.removeClicked = function(file) {
                console.log(file);
                var confirm = $mdDialog.confirm()
                    .title("Delete file")
                    .textContent("Are you sure you want to delete this file?")
                    .ok("Delete")
                    .cancel("Cancel");
                $mdDialog.show(confirm).then(
                    function(ev) {
                        console.log("deleting file");
                        $http.delete("/api/files", file).then(
                            function(response) {
                                console.log(response);
                                ctrl.updateFiles();
                            },
                            function(error) {
                                console.log(error);
                                ctrl.updateFiles();
                            }
                        );
                    }
                );
            };

            ctrl.showUpload = function(ev) {
                var useFullScreen = ($mdMedia('sm') || $mdMedia('xs'))  && $scope.customFullscreen;
                $mdDialog.show({
                    controller: "uploadController",
                    templateUrl: 'upload',
                    parent: angular.element(document.body),
                    targetEvent: ev,
                    clickOutsideToClose:true,
                    openFrom: document.getElementsByClassName("upload-button"),
                    fullscreen: useFullScreen
                });
            }
        }
    ]);