import errors
import uuid
from tornado.web import MissingArgumentError
from email.utils import parseaddr

def __TitleStringChecker(parameter):
    if parameter == None:
        return False
    if not parameter.isalnum():
        return False
    if len(parameter) > 17:
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
            "ProjectId" : {
                "TypeChecker" : __TitleStringChecker,
            },
            "DisplayName" : {
                "TypeChecker" : __ContentStringChecker,
            },
            "Remark" : {
                "TypeChecker" : __ContentStringChecker,
            },
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
