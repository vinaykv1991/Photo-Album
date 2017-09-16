var controllerApp = angular.module('controllerApp', [
    'servicesApp'
]);

controllerApp.controller('AlbumCtrl', function ($scope, $http, serviceProvider, $location) {
    $scope.albums = [];
    $scope.page_load_error = "";
    $scope.new_album = {};
    $scope.add_new_album_error = "";
    $scope.add_new_album_success = "";
    
    serviceProvider.getAlbums(function (err, albums) {
        if (err) {
            $scope.page_load_error = "Unexpected error on loading the albums";
        } else {
            $scope.albums = albums;
            $scope.page_load_error = "";
        }
    });
    
    $scope.addAlbum = function (new_album) {
        serviceProvider.addAlbum(new_album, function (err, album) {
            $scope.add_new_album_error = "";
            $scope.add_new_album_success = "";
            if (err) {
                if (err.code === "title_is_missing") {
                    $scope.add_new_album_error = "Name of the Album is missing";
                } else if (err.code === 'date_is_not_valid') {
                    $scope.add_new_album_error = "Date is not in right format";
                } else if (err.code === 'nickname_is_missing') {
                    $scope.add_new_album_error = "Nick Name of the Album is missing";
                } else if (err.code === 'description_is_missing') {
                    $scope.add_new_album_error = "Description of the Album is missing";
                } else if (err.code === 'duplicate_album_title') {
                    $scope.add_new_album_error = "Album with this name already exists";
                } else {
                    $scope.add_new_album_error = "Unexpected error while adding new album " + err.code + " " + err.message;
                }
            } else {
                $scope.add_new_album_success = "Successfully added a new album into your collection";
                $location.path("/albumview/" + new_album.name);
            }
        });
    };
});

controllerApp.controller('AlbumViewCtrl', function ($scope, $http, $routeParams, serviceProvider) {
    $scope.album_shortname = $routeParams.album_shortname;
    $scope.photos = [];
    $scope.photosExists = false;
    $scope.photo_array_load_error_message = "";
    serviceProvider.getPhotosByName($scope.album_shortname, function (err, data) {
        if (err) {
            $scope.photo_array_load_error_message = "cannot find the album " + err.code + " " + err.message;
        } else {
            $scope.photos = data;
            if ($scope.photos && $scope.photos.length > 0) {
                $scope.photosExists = true;
            }
        }
    });
});

controllerApp.controller('PhotoViewCtrl', function ($scope, $routeParams) {
    $scope.album_shortname = $routeParams.album_shortname;
    $scope.photo_name = $routeParams.photo_name;
});

controllerApp.controller('PhotoUploadCtrl', function ($scope, $routeParams, serviceProvider) {
    $scope.album_shortname = $routeParams.album_shortname;
    $scope.album_load_error_message = "";
    $scope.done_uploading = false;
    $scope.descriptions = {};
    
    serviceProvider.getPhotosByName($scope.album_shortname, function (err, data) {
        if (err) {
            $scope.album_load_error_message = "cannot find the album to upload the photos " + err.code + " " + err.message;
        } else {
            $scope.photos = data;
        }
    });
    
    $scope.uploader = serviceProvider.getUploader($scope.album_shortname, $scope);
    
    $scope.uploader.onCompleteAll = function () {
        $scope.done_uploading = true;
    };
    
    $scope.uploader.onAfterAddingFile = function (item) {
        var fn = _fix_filename(item.file.name);
        var date = item.file.lastModifiedDate;
        var dateString = date.getFullYear() + "/" + date.getMonth() + "/" + date.getDate();
        
        item.formData = [{
            filename: fn, 
            date: dateString,
            description: $scope.descriptions[item.file.name]            
        }];
    };
    
        $scope.uploader.onWhenAddingFileFailed = function(item /*{File|FileLikeObject}*/, filter, options) {
            console.info('onWhenAddingFileFailed', item, filter, options);
        };
        $scope.uploader.onAfterAddingAll = function(addedFileItems) {
            console.info('onAfterAddingAll', addedFileItems);
        };
        $scope.uploader.onProgressItem = function(fileItem, progress) {
            console.info('onProgressItem', fileItem, progress);
        };
        $scope.uploader.onProgressAll = function(progress) {
            console.info('onProgressAll', progress);
        };
        $scope.uploader.onSuccessItem = function(fileItem, response, status, headers) {
            console.info('onSuccessItem', fileItem, response, status, headers);
        };
        $scope.uploader.onErrorItem = function(fileItem, response, status, headers) {
            console.info('onErrorItem', fileItem, response, status, headers);
        };
        $scope.uploader.onCancelItem = function(fileItem, response, status, headers) {
            console.info('onCancelItem', fileItem, response, status, headers);
        };
        $scope.uploader.onCompleteItem = function(fileItem, response, status, headers) {
            console.info('onCompleteItem', fileItem, response, status, headers);
        };
    
    /**
     * we'll be super fussy and only allow alnum, -, _, and .
     */
    function _fix_filename(fn) {
        if (!fn || fn.length == 0)  return "unknown";

        var r = new RegExp("^[a-zA-Z0-9\\-_.]+$");
        var out = "";

        for (var i = 0; i < fn.length; i++) {
            if (r.exec(fn[i]) != null)
                out += fn[i];
        }

        if (!out) out = "unknown_" + (new Date()).getTime();
        return out;
    }
});