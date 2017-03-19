import tornado.web
import filters
import uuid
import data
import json

factory = data.DataFactory()
storage = factory.create("local", '/tmp/easymemo2.redis.sock')

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class ApiServiceHandler(tornado.web.RequestHandler):
    __filters   = [filters.CreateContextFilter, filters.ParameterExistenceFilter, filters.ParameterTypeFilter]

    def create_project(storage, parameters):
        return storage.CreateProject(
            parameters["ProjectId"],
            parameters["DisplayName"],
            parameters["Remark"],
        )

    __apis      = {
        "CreateProject" : create_project,
    }

    def get(self, action):
        for filter in self.__filters:
            res = filter(action, self)
            if res != None:
                self.write_response(res)
                return

        res = self.api_invoke(action)
        self.write_response(res)

    def api_invoke(self, action):
        return self.__apis[action](storage, self.mcontext["parameters"])

    def write_response(self, res):
        if res == None:
            res = {}
        res["RequestId"] = self.mcontext["requestId"]
        self.write(json.dumps(res))

class AboutHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("about.html")
