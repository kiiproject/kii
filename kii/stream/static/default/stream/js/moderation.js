
/* La je recréé l'app à chaque fois pour des raisons de praticité, mais
    dans un vrai code vous auriez ça dans un fichier à part, une seule
    fois */

// change aungular scope delimiter, or it will collide with django templates
// thanks http://www.daveoncode.com/2013/10/17/how-to-make-angularjs-and-django-play-nice-together/
var app = angular.module('moderationApp', []);

app.config(['$httpProvider', '$interpolateProvider',
    function($httpProvider, $interpolateProvider) {
        /* for compatibility with django teplate engine */
        $interpolateProvider.startSymbol('[[');
        $interpolateProvider.endSymbol(']]');
        /* csrf */
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
}]);

// Création d'un controller, et attachement d'une variable au scope.
app.controller('commentCtrl', function($scope, $http){
    // Attachement d'une donnée au scope

    $scope.setStatus = function(event, status) {
        event.preventDefault();
        var url = event.target.attributes.href.value;
        $http({
            method: "patch", 
            url: url,
            data: {'status': status},
        }).
          success(function(data, status, headers, config) {
            // this callback will be called asynchronously
            // when the response is available
            angular.element(event.target).closest('.comment').hide();
          }).
          error(function(data, status, headers, config) {
            // called asynchronously if an error occurs
            // or server returns response with an error status.
            console.log(data);
          });
        
    }

})