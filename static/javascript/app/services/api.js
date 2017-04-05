app.factory('api', function($http, $httpParamSerializer) {
    var api = {
        invoke  : function(url, params) {
            var promise = $http({
                url     : url,
                method  : "POST",
                data    : $httpParamSerializer(params),
                headers : {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(function onSuccess(response) {
                    return response.data;
                }, function onFail(response) {
                    var data     = {
                        Message     : false,
                        RequestId   : response,
                        Code        : "Internal Error"
                    };
                    return data;
                }
            );
            return promise;
        },
        GetUserInfo : function(accessKeyId, accessKeySecret) {
            return {
                UserId : "BillyLiu",
                UserDisplayName : "Billy Liu"
            }
        }
    };
    return api;
});
