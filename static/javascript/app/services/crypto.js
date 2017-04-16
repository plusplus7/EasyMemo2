app.factory('crypto', function() {
    var crypto = {
        hmacsha256 : function(message, secret) {
            return CryptoJS.HmacSHA256(message, secret);
        },
        base64Encode : function(message) {
            return btoa(message);
        },
        base64Decode : function(message) {
            return atob(message);
        },
        __fill : function(str, n) {
            var result = "";
            if (str.length > n) {
                return "";
            }
            for (var i=0; i<n-str.length; i++) {
                result += ' ';
            }
            result += str;
            return result;
        },
        __generateId : function(version, email, timeStart, timeEnd, random, remark, secret) {
            var plaintext = this.__fill(version.toString(16), 1)
                + this.__fill(email, 32)
                + this.__fill((timeStart).toString(16), 16)
                + this.__fill((timeEnd).toString(16), 16)
                + this.__fill(random.toString(16), 7)
                + this.__fill(remark, 8);
            return this.base64Encode(plaintext + this.hmacsha256(plaintext, secret));
        },
        generateCredentialId : function(email, password, remark) {
            var params = {
                version : 0,
                email : email,
                timeStart : Date.now(),
                timeEnd : Date.now() + 3600000,
                random : Math.random().toString(36).substring(2, 9),
                remark : remark,
                secret : this.hmacsha256(email, password).toString()
            };

            if (params.version === 0) {
                return this.__generateId(params["version"],
                    params["email"],
                    params["timeStart"],
                    params["timeEnd"],
                    params["random"],
                    params["remark"],
                    params["secret"]
                )
            }
        },
        generateCredentialSecret : function(email, password, credentialId) {
            var secret = this.hmacsha256(email, password).toString();
            return this.hmacsha256(credentialId, secret).toString();
        }
    };
    return crypto;
});
