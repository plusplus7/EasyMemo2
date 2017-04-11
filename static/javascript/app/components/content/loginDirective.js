app.controller("loginCtrl", function($scope, user) {
    $scope.submit = function () {
        console.log("!");
    };

    $scope.signInOnClick = function(email, password) {
        console.log(email);
        console.log(password);
    };

    $scope.signUpOnClick = function() {
        user.setSigningUp();
    };
});
