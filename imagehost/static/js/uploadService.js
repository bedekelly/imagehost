(function () {
    angular.module("uploadModule")
        .service("uploadService", ["$http", UploadService]);

    function UploadService($http) {
        function uploadFiles(files, onSuccess, onFail) {
            var formData = new FormData();
            angular.forEach(files, function (obj) {
                formData.append("files[]", obj.lfFile);
            });
            var self = this;
            self.status = "success";
            $http.post("/api/upload", formData, {
                transformRequest: angular.identity,
                headers: {"Content-Type": undefined}
            }).then(onSuccess, onFail);
            return self.status;
        }

        return {
            uploadFiles: uploadFiles
        }
    }
})();

