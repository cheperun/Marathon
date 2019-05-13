#!/usr//bin/env python2

import sys, time

import logging
#import logging.config
import tornado.ioloop
import tornado.web, tornado.options
import slice
import json
from slice_manager import *
import hydra
import xmlrpclib


logging.getLogger().setLevel(logging.INFO)

class add(tornado.web.RequestHandler):
    def initialize(self,slices):
        self.slices=slices

    def get(self):
        self.render("templates/addslice.html")
        

    def post(self):
        
        rs_name=self.get_argument('rs_name')
        nep_vbs = self.get_argument('nep_vbs')
        nep_vue = self.get_argument('nep_vue')
        channelbw_min=self.get_argument('channelbw_min')
        channelbw_max=self.get_argument('channelbw_max')
        channelsharingpool=self.get_argument('channelsharingpool')
        chairpolicy=self.get_argument('chairpolicy')
        chairminratio=self.get_argument('chairminratio')
        chairmaxratio=self.get_argument('chairmaxratio')
        chairavgint=self.get_argument('chairavgint')
        res_id_1=self.slices.exist_slice("1")
        res_id_2=self.slices.exist_slice("2")
        res_id_3=self.slices.exist_slice("3")
        if not res_id_1:
            id="1"
            logging.info("Processing Slice Attributes. Deciding what to send to the corresponding Hydra clients, VBS and VUE")
            logging.info("Configuration of Hydra client1 or client2")
            logging.info("Configuration of vbs")
            logging.info("Configuration of vue1, vue2 or vue3")
        elif not res_id_2:
            id="2"
            logging.info("Processing Slice Attributes. Deciding what to send to the corresponding Hydra clients, VBS and VUE")
            logging.info("Configuration of Hydra client1 or client2")
            logging.info("Configuration of vbs")
            logging.info("Configuration of vue1, vue2 or vue3")
            
        elif not res_id_3:
            id="3"
            logging.info("Processing Slice Attributes. Deciding what to send to the corresponding Hydra clients, VBS and VUE")
            logging.info("Configuration of Hydra client1 or client2")
            logging.info("Configuration of vbs")
            logging.info("Configuration of vue1, vue2 or vue3")
            
        else:
            id="0"
        if id == "0":
            self.render("templates/error_ad.html",id=id)
            print "Error. Slice" +id+ " exist" 
        else:    
            slic = {
                "id" : id,
                "rs_name" : rs_name,
                "nep_vbs" : nep_vbs,
                "nep_vue" : nep_vue,
                "channelbw_min" : channelbw_min,
                "channelbw_max" : channelbw_max,
                "channelsharingpool": channelsharingpool,
                "chairpolicy" : chairpolicy,
                "chairminratio": chairminratio,
                "chairmaxratio" : chairmaxratio,
                "chairavgint" : chairavgint,
            }
            print id
            result=self.slices.add_slice(id,rs_name,nep_vbs,nep_vue,channelbw_min,channelbw_max,channelsharingpool,chairpolicy,chairminratio,chairmaxratio,chairavgint)
            logging.info("El Slice  ha sido introducido Correctamente")
            self.render("templates/addslice2.html",id=id)


            
            
            