angular.module("uploadModule")
    .controller("uploadController", ["uploadService", "$mdToast", function(uploadService, $mdToast) {
        var self = this;  // Keep a handle to the controller.
        // Instead of using "$scope", keep everything in the controller.
        // Use "templateController as tc" and then tc.whatever is available.

        // Write your controller methods here!
        self.files = [];

        self.onSubmit = function() {
            if (self.files == false) {
                $mdToast.showSimple("Choose a file to upload!");
                return;
            }
            uploadService.uploadFiles(self.files, self.showCompleteToast, self.showTooLargeToast);
        };

        self.showTooLargeToast = function() {
            $mdToast.showSimple("File size too large! (Max 16MB");
        };

        self.showCompleteToast = function() {
            $mdToast.showSimple("File uploaded successfully!");
            self.fileInputAPI.removeAll();
        }
    }]);