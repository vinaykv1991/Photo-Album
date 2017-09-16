var servicesApp = angular.module('servicesApp', [
    'angularFileUpload'
]);

servicesApp.service('serviceProvider', function ($http, FileUploader) {
    
    
    this.getUploader = function(album_name, scope) {
        return new FileUploader({
            scope: scope,
            method: 'put',
            url: '/v1/albums/'+album_name+'/photos.json'
        });
    }
    
    this.getAlbums = function (callback) {
        $http.get('/v1/albums.json').success(function (data, status) {
            callback(null, data);
        }).error(function (data, status) {
            callback(data);
        });
    };
    
    this.getPhotosByName = function (album_name, callback) {
        $http.get('/v1/albums/'+album_name+'/photos.json').success(function (data, status) {
            callback(null,data);
        }).error (function (data, status){
            callback(data);
        });
    };
    
    this.addAlbum = function (new_album, callback) {
        
        if (!new_album.title) {
            callback({code: "title_is_missing"});
        }
        if (!new_album.date) {
            callback({code: "date_is_not_valid"});
        }
        if (!new_album.name) {
            callback({code: "nickname_is_missing"});
        }
        if (!new_album.description) {
            callback({code: "description_is_missing"});
        }
        
        $http.put('/v1/albums.json', new_album).success(function (data, status) {
            callback(null,data);
        }).error(function (data,status) {
           callback(data); 
        });
    };
});