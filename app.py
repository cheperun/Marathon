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
from slice_manager import Slice
import hydra
import xmlrpclib
import logging
import logging.config

slices=Slices()
def main():
    
    
    #client1 = hydra.hydra_client("192.168.5.70", 5000, 1, True)
    #ue1 = xmlrpclib.ServerProxy("http://192.168.5.78:8080")
    #client2 = hydra.hydra_client("192.168.5.70", 5000, 1, True)
    #ue2 = xmlrpclib.ServerProxy("http://192.168.5.78:8080")
    


    ## IMPORTANT: The script ansible_hydra_client_2tx_2rx already allocated resources for traNsmission and reception
    ##            These resources are under the use of clients ID 1 and ID 2. The trick of this script is to connect
    #           with the server using the same ID (1 and 2), and them releasing the resources allocated.
    #           We can then allocate new resources from this python without impacting the slices. 
    


    #Start Hydra Clients          
    # We put the IP of the machine executing this script
    
    #client1 = hydra.hydra_client("192.168.5.70", 5000, 1, True)
    #if client1.check_connection(3) == "":
    #    print("client1 could not connect to server")
    #    sys.exit(1)
    logging.info("Hydra client 1 connected to server")


    # We put the IP of the machine executing this script
    #client2 = hydra.hydra_client("192.168.5.70", 5000, 2, True)
    #if client2.check_connection(3) == "":
    #    print("client2 could not connect to server")
    #    sys.exit(1)
    logging.info("Hydra client 2 connected to server")


    #Start VBS Connection
    logging.info("VBS connection established")



    #Start VUE Connections 
    # We put the IP of the machine running the UE
    #vue1 = xmlrpclib.ServerProxy("http://192.168.5.78:8080")
    logging.info("VUE#1 connection established")

    # We put the IP of the machine running the UE
    
    logging.info("VUE#2 connection established")

    # We put the IP of the machine running the UE
    
    logging.info("VUE#3 connection established")
    
    

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
    main()
    app2.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
    logging.info("Web server started. Listening in port 8888")