app.factory('crypto', function() {
    var crypto = {
        hmacsha256 : function(message, secret) {
            return CryptoJS.HmacSHA256(message, secret);
        }
    };
    return crypto;
});
