
/* La je recréé l'app à chaque fois pour des raisons de praticité, mais
    dans un vrai code vous auriez ça dans un fichier à part, une seule
    fois */

// change aungular scope delimiter, or it will collide with django templates
// thanks http://www.daveoncode.com/2013/10/17/how-to-make-angularjs-and-django-play-nice-together/
var app = angular.module('tuto', [], function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});

// Création d'un controller, et attachement d'une variable au scope.
app.controller('HelloCtrl', function($scope){
    // Attachement d'une donnée au scope
    $scope.hello = "Hello"
})