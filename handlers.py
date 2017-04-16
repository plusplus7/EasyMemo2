import tornado.web
import filters
import errors
import uuid
import data
import json
import utils

factory = data.DataFactory()
storage = factory.create("local", '/tmp/easymemo2.redis.sock')

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class ApiServiceHandler(tornado.web.RequestHandler):
    # TODO: should be some other way to do it
    __verifies = ["00000000-0000-0000-0000-000000000000"]

    def create_project(storage, parameters, userInfo):
        projectId = str(uuid.uuid4())
        res = storage.CreateProject(
            projectId,
            parameters["DisplayName"],
            parameters["Remark"],
        )
        if res != None:
            return res
        return storage.AttachProjectToUser(projectId, userInfo["email"])

    def create_entity(storage, parameters, userInfo):
        return storage.CreateEntity(
            parameters["ProjectId"],
            parameters["EntityId"],
            parameters["DisplayName"],
            parameters["Currency"],
            float(parameters["Balance"]),
            parameters["Remark"],
        )

    def create_log(storage, parameters, userInfo):
        return storage.CreateLog(
            parameters["ProjectId"],
            parameters["LogId"],
            parameters["EntityOut"],
            parameters["EntityIn"],
            float(parameters["Amount"]),
            parameters["Tag"],
            parameters["Remark"],
        )

    def query_entity(storage, parameters, userInfo):
        return storage.QueryEntity(

        )

    def verify_user(storage, parameters):
        user = storage.QueryUser(parameters["EmailAddress"])
        if user in errors.errors:
            return user

        if utils.VerifyUserCredentialId(parameters["CredentialId"], user["Secret"]) == False:
            return errors.AccessForbidden
        return {}

    def get_user_info(storage, parameters, userInfo):
        result = storage.QueryUser(parameters["EmailAddress"])
        if result in errors.errors:
            return result
        del result["Secret"]
        return result

    def register_user(storage, parameters):
        if parameters["VerificationCode"] not in ApiServiceHandler.__verifies:
            return errors.OperationFailed

        ApiServiceHandler.__verifies.remove(parameters["VerificationCode"])
        ApiServiceHandler.__verifies.append(str(uuid.uuid4()))
        print ApiServiceHandler.__verifies

        return storage.CreateUser(
            parameters["EmailAddress"],
            parameters["NickName"],
            parameters["Secret"]
        )

    __apis      = {
        "CreateProject" : create_project,
        "CreateEntity"  : create_entity,
        "CreateLog"     : create_log,
        "RegisterUser"  : register_user,
        "VerifyUser"    : verify_user,
        "GetUserInfo"   : get_user_info,
    }
    __filters   = {

        "CreateProject" : [filters.CreateContextFilter, filters.ParameterExistenceFilter, filters.ParameterTypeFilter, filters.AuthenticationFilter],
        "CreateEntity"  : [filters.CreateContextFilter, filters.ParameterExistenceFilter, filters.ParameterTypeFilter, filters.AuthenticationFilter],
        "CreateLog"     : [filters.CreateContextFilter, filters.ParameterExistenceFilter, filters.ParameterTypeFilter, filters.AuthenticationFilter],
        "RegisterUser"  : [filters.CreateContextFilter, filters.ParameterExistenceFilter, filters.ParameterTypeFilter],
        "VerifyUser"    : [filters.CreateContextFilter, filters.ParameterExistenceFilter, filters.ParameterTypeFilter],
        "GetUserInfo"   : [filters.CreateContextFilter, filters.ParameterExistenceFilter, filters.ParameterTypeFilter, filters.AuthenticationFilter],
    }

    def post(self, action):
        for filter in self.__filters[action]:
            res = filter(action, self)
            if res != None:
                self.write_response(res)
                return

        res = self.api_invoke(action)
        self.write_response(res)

    def api_invoke(self, action):
        if filters.AuthenticationFilter in self.__filters[action]:
            return self.__apis[action](storage, self.mcontext["parameters"], self.mcontext["userInfo"])
        else:
            return self.__apis[action](storage, self.mcontext["parameters"])


    def write_response(self, res):
        if res == None:
            res = {}
        elif res in errors.errors:
            self.write(json.dumps(res))
            return
        res["RequestId"] = self.mcontext["requestId"]
        res["Code"] = 200
        self.write(json.dumps(res))

class AboutHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("about.html")
