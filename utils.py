import hmac
import hashlib
import base64

def base64Decode(message):
    return base64.b64decode(message)

def base64Encode(message):
    return base64.b64encode(message)

def hmacsha256(message, secret):
    return hmac.new(key=str(secret), msg=str(message), digestmod=hashlib.sha256).hexdigest()

def GetInfoFromCredentialId(credentialIdB64):
    if credentialIdB64 == None:
        return None
    credentialId =  base64.b64decode(credentialIdB64)
    version = int(credentialId[0], 16)
    if version not in [0]:
        return None

    if version == 0:
        email = credentialId[1:33].strip()
        timeStart = int(credentialId[33:49].strip(), 16)
        timeEnd = int(credentialId[49:65].strip(), 16)
        random = credentialId[65:72].strip()
        remark = credentialId[72:80].strip()

        return {
            "email" : email,
            "timeStart" : timeStart,
            "timeEnd" : timeEnd,
            "random" : random,
            "remark" : remark
        }
    return None

def VerifyUserCredentialId(credentialIdB64, secret):
    if credentialIdB64 == None:
        return False
    credentialId =  base64.b64decode(credentialIdB64)
    version = int(credentialId[0], 16)
    if version not in [0]:
        return False

    if version == 0:
        plaintext = credentialId[0:80]
        hashtext = credentialId[80:]
    return hmacsha256(plaintext, secret) == hashtext

def GenerateCredentialSecret(credentialId, secret):
    return hmacsha256(credentialId, secret)
