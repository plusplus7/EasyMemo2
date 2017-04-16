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
        Sign : function(action, param, secret) {
            var strToSign = "" + action + "\n";
            var keys = [];
            for(var key in param)
                keys.push(key);
            keys = keys.sort();
            for (var i in keys) {
                var key = keys[i];
                strToSign = strToSign + key + ":" + crypto.base64Encode(param[key]) + "\n";
            }
            console.log(strToSign);
            return crypto.hmacsha256(crypto.base64Encode(strToSign), secret).toString();
        },
        CreateProject : function(displayName, remark, credentialId, credentialSecret) {
            var param = {
                "DisplayName" : displayName,
                "Remark" : remark,
            };
            param["Signature"] = this.Sign("CreateProject", param, credentialSecret);
            param["CredentialId"] = credentialId;
            return this.invoke("/api/CreateProject", param);
        },
        GetUserInfo : function(email, credentialId, credentialSecret) {
            var param = {
                "EmailAddress" : email,
            };
            param["Signature"] = this.Sign("GetUserInfo", param, credentialSecret);
            param["CredentialId"] = credentialId;
            return this.invoke("/api/GetUserInfo", param);
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
                    alert('The length of e-mail address is too long ( greater than 32 letters).');
                }
            } else {
                alert('Passwords are required to be the same!');
            }
        },
        VerifyUser : function(email, credentialId) {
            var param = {
                "EmailAddress" : email,
                "CredentialId" : credentialId
            };
            return this.invoke("/api/VerifyUser", param);
        }

    };
    return api;
});
