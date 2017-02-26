import tornado.web

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class ApiServiceHandler(tornado.web.RequestHandler):
    def get(self, action):
        self.write("ok")

class AboutHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("about.html")
