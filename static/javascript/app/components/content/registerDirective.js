app.controller("registerCtrl", function($scope, api, user) {
    $scope.signUpOnClick = function(email, password, passwordConfirmed, verificationCode) {
        console.log(email);
        console.log(password);
        console.log(passwordConfirmed);
        console.log(verificationCode);
        api.RegisterUser(email, password, passwordConfirmed, verificationCode).then(function(result) {
            if (result.Code === 200) {
                alert('Success!');
                user.setSigningIn();
            } else {
                alert('Failed!\n' + result.Message);
            }
        });
    };
    $scope.sendVerificationCode = function(email) {
        alert('Sorry. This website is currently available for public.\nPlease contact administrator[ huangyifeng001 @ yeah.net ] for invitation.');
    }
});
