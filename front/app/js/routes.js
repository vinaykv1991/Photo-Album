var routesModule = angular.module('routesModule', [
    'ngRoute'
]);
routesModule.config(function ($routeProvider) {
    $routeProvider
        .when('/view', {
            templateUrl: "partials/view.html",
            controller: "AlbumCtrl"
        })
        .when('/albumview/:album_shortname', {
            templateUrl: "partials/albumview.html",
            controller: "AlbumViewCtrl"
        })
        .when('/albumview/:album_shortname/upload', {
            templateUrl: "partials/photoUpload.html",
            controller: "PhotoUploadCtrl"
        })
        .when('/albumview/:album_shortname/:photo_name', {
            templateUrl: "partials/photoview.html",
            controller: "PhotoViewCtrl"
        })
        .otherwise({
            templateUrl: "partials/view.html",
            controller: "AlbumCtrl"
        });
});