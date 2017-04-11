/**
 * Created by plusplus7 on 2017/4/6.
 */

app.factory('user', function() {
    var user = {
        __status : "init",
        isAuthenticated : function() {
            return this.__status==="authenticated";
        },
        isSigningUp : function() {
            return this.__status==="signingUp";
        },
        setSigningUp : function() {
            this.__status = "signingUp";
        },
        setAuthenticated : function() {
            this.__status = "authenticated";
        },
        email  : "",
        password : "",
        accessKeyId : "",
        accessKeySecret : ""
    };
    return user;
});

