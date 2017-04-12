app.controller("registerCtrl", function($scope, api) {
    $scope.sendVerificationCode = function(email) {
        console.log(email);
    };
    $scope.signUpOnClick = function(email, password, passwordConfirmed, verificationCode) {
        console.log(email);
        console.log(password);
        console.log(passwordConfirmed);
        console.log(verificationCode);
        api.RegisterUser(email, password, passwordConfirmed, verificationCode).then(function(result) {
            console.log(result);
        });
    };
    $scope.sendVerificationCode = function(email) {
        console.log(email);
        alert('Sorry. This website is currently available for public.\nPlease contact administrator[ huangyifeng001 @ yeah.net ] for invitation.');
    }
});
