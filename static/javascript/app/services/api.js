app.factory('api', function($http, $httpParamSerializer, crypto) {
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
        },
        RegisterUser : function(email, password, passwordConfirmed, verificationCode) {
            var param = {
                "EmailAddress"      : email,
                "NickName"          : email.split('@')[0],
                "VerificationCode"  : verificationCode
            };
            if (password === passwordConfirmed) {
                if (email.length <= 32) {
                    param["Secret"] = crypto.hmacsha256(email, password).toString();
                    return this.invoke("/api/RegisterUser", param);
                } else {
                    alert('The length of e-mail address is too long ( greater than 32 letters).')
                }
            } else {
                alert('Passwords are required to be the same!')
            }
        }
    };
    return api;
});
