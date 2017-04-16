import errors
import uuid
import utils
from tornado.web import MissingArgumentError
from email.utils import parseaddr
import data
import time

factory = data.DataFactory()
storage = factory.create("local", '/tmp/easymemo2.redis.sock')

def __TitleStringChecker(parameter):
    if parameter == None:
        return False
    if not parameter.isalnum():
        return False
    if len(parameter) > 17:
        return False
    return True

def __CredentialStringChecker(parameter):
    if parameter == None:
        return False
    if len(parameter) > 200:
        return False
    return True

def __PasswordStringChecker(parameter):
    if parameter == None:
        return False
    if not parameter.isalnum():
        return False
    if len(parameter) > 64:
        return False
    return True

def __EmailStringChecker(parameter):
    if len(parameter) > 32:
        return False
    return '@' in parseaddr(parameter)[1]

def __UUIDStringChecker(parameter):
    try:
        val = uuid.UUID(parameter, version=4)
    except ValueError:
        return False
    return True

def __ContentStringChecker(parameter):
    if parameter == None:
        return False
    if not parameter.isalnum():
        return False
    if len(parameter) > 37:
        return False
    return True

def __CurrencyChecker(parameter):
    if parameter == None:
        return False
    if not parameter.isupper():
        return False
    if len(parameter) > 5:
        return False
    return True

def __FloatNumberChecker(parameter):
    try:
        float(parameter)
    except ValueError:
        return False
    return True

# TODO: can be a dynamic configuration

apis = {
    "CreateProject" : {
        "parameters" : {
            "DisplayName" : {
                "TypeChecker" : __ContentStringChecker,
            },
            "Remark" : {
                "TypeChecker" : __ContentStringChecker,
            },
            "CredentialId" : {
                "TypeChecker" : __CredentialStringChecker,
            },
            "Signature" : {
                "TypeChecker" : __CredentialStringChecker,
            }
        }
    },
    "CreateEntity" : {
        "parameters" : {
            "ProjectId" : {
                "TypeChecker" : __TitleStringChecker,
            },
            "EntityId" : {
                "TypeChecker" : __TitleStringChecker,
            },
            "DisplayName" : {
                "TypeChecker" : __ContentStringChecker,
            },
            "Currency" : {
                "TypeChecker" : __CurrencyChecker,
            },
            "Balance" : {
                "TypeChecker" : __FloatNumberChecker,
            },
            "Remark" : {
                "TypeChecker" : __ContentStringChecker,
            },
        }
    },
    "CreateLog" : {
        "parameters" : {
            "ProjectId" : {
                "TypeChecker" : __TitleStringChecker,
            },
            "LogId" : {
                "TypeChecker" : __TitleStringChecker,
            },
            "EntityOut" : {
                "TypeChecker" : __TitleStringChecker,
            },
            "EntityIn" : {
                "TypeChecker" : __TitleStringChecker,
            },
            "Amount" : {
                "TypeChecker" : __FloatNumberChecker,
            },
            "Tag" : {
                "TypeChecker" : __ContentStringChecker,
            },
            "Remark" : {
                "TypeChecker" : __ContentStringChecker,
            },
        }
    },
    "RegisterUser" : {
        "parameters" : {
            "EmailAddress" : {
                "TypeChecker" : __EmailStringChecker,
            },
            "NickName" : {
                "TypeChecker" : __ContentStringChecker,
            },
            "Secret" : {
                "TypeChecker" : __PasswordStringChecker,
            },
            "VerificationCode" : {
                "TypeChecker" : __UUIDStringChecker,
            },
        }
    },
    "VerifyUser" : {
        "parameters" : {
            "EmailAddress" : {
                "TypeChecker" : __EmailStringChecker,
            },
            "CredentialId" : {
                "TypeChecker" : __CredentialStringChecker,
            },
        }
    },
    "GetUserInfo" : {
        "parameters" : {
            "EmailAddress" : {
                "TypeChecker" : __EmailStringChecker,
            },
            "CredentialId" : {
                "TypeChecker" : __CredentialStringChecker,
            },
            "Signature" : {
                "TypeChecker" : __CredentialStringChecker,
            }
        }
    }
}

def CreateContextFilter(action, handler):
    if action not in apis.keys():
        return errors.ActionNotSupported

    handler.mcontext = {
        "requestId" : str(uuid.uuid4()),
        "parameters" : {},
    }
    return None

def ParameterExistenceFilter(action, handler):
    context = handler.mcontext

    for param in apis[action]["parameters"].keys():
        try:
            context["parameters"][param] = handler.get_argument(param)
        except MissingArgumentError:
            return errors.ParameterNotExists
    return None

def ParameterTypeFilter(action, handler):
    context = handler.mcontext

    for param in apis[action]["parameters"].keys():
        value = handler.get_argument(param)
        if not apis[action]["parameters"][param]["TypeChecker"](handler.get_argument(param)):
            return errors.InvalidParameter
        context["parameters"][param] = value
    return None

def AuthenticationFilter(action, handler):
    keys = sorted(handler.mcontext["parameters"].keys())

    strToSign = "" + action + "\n"
    for param in keys:
        if param == "CredentialId" or param == "Signature":
            continue
        strToSign = strToSign + param + ":" + utils.base64Encode(handler.mcontext["parameters"][param]) + "\n"

    strToSign = utils.base64Encode(strToSign)
    credentialIdB64 = handler.mcontext["parameters"]["CredentialId"]
    info = utils.GetInfoFromCredentialId(credentialIdB64)
    secret = storage.QueryUser(info["email"])
    if secret in errors.errors:
        return secret
    secret = secret["Secret"]
    key = utils.GenerateCredentialSecret(credentialIdB64, secret)
    signature = utils.hmacsha256(strToSign, key)

    """
    print info["timeStart"]
    print int(time.time()*1000)
    print info["timeEnd"]
    print signature
    print handler.mcontext["parameters"]["Signature"]
    """
    if info["timeStart"] < int(time.time()*1000) and \
        info["timeEnd"] > int(time.time()*1000) and \
        signature == handler.mcontext["parameters"]["Signature"]:
        handler.mcontext["userInfo"] = info
        return None
    return errors.AccessForbidden
