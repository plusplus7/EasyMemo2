app.controller("registerCtrl", function($scope, user) {
    $scope.sendVerificationCode = function(email) {
        console.log(email);
    };
    $scope.signUpOnClick = function(email, password, passwordConfirmed, verificationCode) {
        console.log(email);
    };
});
