app.controller("loginCtrl", function($scope, crypto, api, user) {
    $scope.submit = function () {
        console.log("!");
    };

    $scope.signInOnClick = function(email, password) {
        var credentialId =  crypto.generateCredentialId(email, password, "remark");
        api.VerifyUser(email, credentialId).then(function (result) {
            if (result.Code === 200) {
                console.log(email);
                console.log(password);
                user.__generateCredentials(email, password);
                user.setAuthenticated();
                user.saveStatus();
            } else {
                alert('Wrong password. Please try again.');
            }
        });
    };

    $scope.signUpOnClick = function() {
        user.setSigningUp();
    };
});
