import sys, time

import tornado.ioloop
import tornado.web, tornado.options

class HelloWorld(tornado.web.RequestHandler):
    def get(self):
        self.write("Welcome to Marathon Project Web")

settings = {
    "debug": True,
    "autoreload": True,
    
}
app2 = tornado.web.Application([
    (r"/", HelloWorld),
    
    
], **settings )
if __name__ == "__main__":
    app2.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
    logging.info("Web server started. Listening in port 8888")
