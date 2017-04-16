app.controller("userinfoCtrl", function($scope, api, user) {
    user.addStatusListener("UserInfoListener", function(newStatus) {
        console.log(newStatus);
        api.GetUserInfo(user.email, user.credentialId, user.credentialSecret).then(function(result) {
            console.log(result);
            if (result.Code === 200) {
                $scope.data = {
                    UserDisplayName: result.UserId,
                    Projects : result.Projects,
                    activeProject : null
                };
                if ($scope.data.Projects.length > 0) {
                    $scope.data.activeProject = $scope.data.Projects[0].ProjectId;
                }
                console.log($scope.data.Projects.length);
            } else {
                alert('There is something wrong with system. Please contact administrator.');
            }
        });
    });
    $scope.newProjectOnClick = function(displayName, remark) {
        api.CreateProject(displayName, remark, user.credentialId, user.credentialSecret).then(function(result) {
            console.log(result);
            if (result.Code === 200) {
                alert("Success");
            } else {
                alert(result.Message);
            }
        });
    }
});
