import tornado.web
import slice
import json

class modify(tornado.web.RequestHandler):
    def initialize(self, slices):
        self.slices = slices
    
    def get(self):
        id=self.get_argument("option")
        result=self.slices.get_slice(id)
        y=json.loads(result)
        self.render("templates/modify.html",y=y)
        
        

    def post(self):
        id=self.get_argument('id')
        self.slices.update_key('nep_vbs',self.get_argument('nep_vbs'),id)
        self.slices.update_key('nep_vbs',self.get_argument('nep_vbs'),id)
        self.slices.update_key('nep_vue',self.get_argument('nep_vue'),id)
        self.slices.update_key('channelbw_min',self.get_argument('channelbw_min'),id)
        self.slices.update_key('channelbw_max',self.get_argument('channelbw_max'),id)
        self.slices.update_key('sharingpool',self.get_argument('channelsharingpool'),id)
        self.slices.update_key('chairpolicy',self.get_argument('chairpolicy'),id)
        self.slices.update_key('chairminratio',self.get_argument('chairminratio'),id)
        self.slices.update_key('chairmaxratio',self.get_argument('chairmaxratio'),id)
        self.slices.update_key('chairavgint',self.get_argument('chairavgint'),id)
        self.render("templates/modify2.html",id=id)
