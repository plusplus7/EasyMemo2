import tornado.web
import tornado.ioloop
import os
from handlers import *

urls = [
    (r'/',      IndexHandler),
    (r'/api/(?P<action>[a-zA-Z0-9-_]+)', ApiServiceHandler),
    (r'/about', AboutHandler),
]

settings = {
    "static_path"   : os.path.join(os.path.dirname(__file__), "static"),
    "template_path" : os.path.join(os.path.dirname(__file__), "templates"),
    "debug"         : False,
    "gzip"          : True,
    "cookie_secret" : "asdf"
}

def main(addr):
    application = tornado.web.Application(urls, **settings)
    application.listen(8080, addr)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main("127.0.0.1")
