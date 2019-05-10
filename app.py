import sys, time

import tornado.ioloop
import tornado.web, tornado.options
import json
import os
from addslice import add
from getslice import get
from delslice import delete
from modify import modify
from view import view
from slice import Slices
slices=Slices()
settings = {
    "debug": True,
    "autoreload": True,
    "static_path": os.path.join(os.path.dirname(__file__), "css")
    
}
app2 = tornado.web.Application([
    (r"/addslice", add, dict(slices = slices)),
    (r"/", get, dict(slices = slices)),
    (r"/modifyslice", modify, dict(slices = slices)),
    (r"/viewslice", view, dict(slices = slices)),
    (r"/delslice", delete, dict(slices = slices)),
    
    
], **settings )
if __name__ == "__main__":
    #main()
    app2.listen(8888)
    tornado.ioloop.IOLoop.instance().start()