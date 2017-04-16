/**
 * Created by plusplus7 on 2017/4/6.
 */

app.factory('user', function(crypto, $cookies) {
    var user = {
        __status : "signingIn",
        email: "",
        credentialId: "",
        credentialSecret : "",
        listener : {},
        saveStatus : function() {
            $cookies.put('__status', this.__status);
            $cookies.put('email', this.email);
            $cookies.put('credentialId', this.credentialId);
            $cookies.put('credentialSecret', this.credentialSecret);
        },
        loadStatus : function() {
            console.log($cookies.get('__status'));
            if ($cookies.get('__status') === undefined
                || $cookies.get('email') === undefined
                || $cookies.get('credentialId') === undefined
                || $cookies.get('credentialSecret') === undefined)
                return null;
            this.__status           = $cookies.get('__status');
            this.email              = $cookies.get('email');
            this.credentialId       = $cookies.get('credentialId');
            this.credentialSecret   = $cookies.get('credentialSecret');
        },
        addStatusListener : function(name, action) {
            this.listener[name] = action;
            action(this.__status);
        },
        setStatus : function(newStatus) {
            this.__status = newStatus;
            for (var name in this.listener) {
                this.listener[name](newStatus);
            }
        },
        isSigningIn : function() {
            return this.__status==="signingIn";
        },
        isAuthenticated : function() {
            return this.__status==="authenticated";
        },
        isSigningUp : function() {
            return this.__status==="signingUp";
        },
        setSigningIn : function() {
            this.setStatus("signingIn");
        },
        setAuthenticated : function() {
            this.setStatus("authenticated");
        },
        setSigningUp : function() {
            this.setStatus("signingUp");
        },
        __generateCredentials : function(email, password) {
            this.email = email;
            this.credentialId = crypto.generateCredentialId(email, password, "remark");
            this.credentialSecret= crypto.generateCredentialSecret(email, password, this.credentialId);
        }
    };
    user.loadStatus();
    return user;
});

