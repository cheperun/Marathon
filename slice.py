import json


class Slices:

    def __init__(self):
        self.slices = []

    def add_slice(self,id,rs_name,nep_vbs,nep_vue,channelbw_min,channelbw_max,sharingpool,chairpolicy,chairminratio,chairmaxratio,chairavgint):
        sli = {}
        sli["id"]=id
        sli["rs_name"]=rs_name
        sli["nep_vbs"]=nep_vbs
        sli["nep_vue"]=nep_vue
        sli["channelbw_min"]=channelbw_min
        sli["channelbw_max"]=channelbw_min
        sli["sharingpool"]=sharingpool
        sli["chairpolicy"]=chairpolicy
        sli["chairminratio"]=chairminratio
        sli["chairmaxratio"]=chairmaxratio
        sli["chairavgint"]=chairavgint
        self.slices.append(sli)
        return json.dumps(sli)

    def del_slice(self, id):
        found = False
        for idx, slice in enumerate(self.slices):
            if slice["id"] == id:
                index = idx
                found = True
                del self.slices[idx]
        
        return found

    def get_all_slices(self):
        return self.slices
    
    def exist_slice(self,id):
        found= False
        for idx, slice in enumerate(self.slices):
            if slice["id"] == id:
                found = True
        return found

    def get_slice(self, id):
        
        for idx, slice in enumerate(self.slices):
            if slice["id"] == id:
                sli={}
                sli["id"]=slice["id"]
                sli["rs_name"]=slice["rs_name"]
                sli["nep_vbs"]=slice["nep_vbs"]
                sli["nep_vue"]=slice["nep_vue"]
                sli["channelbw_min"]=slice["channelbw_min"]
                sli["channelbw_max"]=slice["channelbw_min"]
                sli["sharingpool"]=slice["sharingpool"]
                sli["chairpolicy"]=slice["chairpolicy"]
                sli["chairminratio"]=slice["chairminratio"]
                sli["chairmaxratio"]=slice["chairmaxratio"]
                sli["chairavgint"]=slice["chairavgint"]
        return json.dumps(sli)
    
    def update_key(self,key,value,id):
       
       for idx, slice in enumerate(self.slices):
           if slice["id"] == id:
               index=idx
               self.slices[index][key]= value


    def json_list(self):
        return json.dumps(self.slices)
