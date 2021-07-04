#!/usr/bin/env python

import tornado.ioloop
import tornado.web
import pprint
import os

class MyDumpHandler(tornado.web.RequestHandler):
    def post(self):
        pprint.pprint(self.request)
        pprint.pprint(self.request.headers['Authorization'])

    def get(self):
        pprint.pprint(self.request)
        pprint.pprint(self.request.headers['Authorization'])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(
        tornado.web.Application([(r"/.*", MyDumpHandler),]),
        ssl_options = {
            "certfile": os.path.join("server.crt"),
            "keyfile": os.path.join("server.key"),
        })
    
    http_server.listen(443)
    tornado.ioloop.IOLoop.instance().start()
