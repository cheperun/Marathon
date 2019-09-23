import json
import sys, time
import hydra
import xmlrpclib
import logging
import logging.config

contshared=0
contnonshared=0
f=open("marathon.txt","r")
f1=f.readlines()
for x in f1:
    letra=x.split("-")
    if (letra[0]=="SERVER"):
        hydra_server = letra[1]
        #print hydra_server
    elif (letra[0]=="VBS"):
        vbs = letra[1]
        #print vbs
    elif (letra[0]=="VUE1"):
        vue1 = letra[1]
        #print vue1
    elif (letra[0]=="VUE2"):
        vue2 = letra[1]
        #print vbs
    elif (letra[0]=="VUE3"):
        vue3 = letra[1]
        #print vue3
        

class Slice_Param:

    def __init__(self):
        self.slices = []

    def add_slice(self,id,rs_name,nep_vbs,nep_vue,channelbw_min,channelbw_max,sharingpool,chairpolicy,chairminratio,chairmaxratio,chairavgint):
        sli_add = {}
        sli_add["id"]=id
        sli_add["rs_name"]=rs_name
        sli_add["nep_vbs"]=nep_vbs
        sli_add["nep_vue"]=nep_vue
        sli_add["channelbw_min"]=channelbw_min
        sli_add["channelbw_max"]=channelbw_max
        sli_add["sharingpool"]=sharingpool
        sli_add["chairpolicy"]=chairpolicy
        sli_add["chairminratio"]=chairminratio
        sli_add["chairmaxratio"]=chairmaxratio
        sli_add["chairavgint"]=chairavgint
        self.slices.append(sli_add)
        return json.dumps(sli_add)

    def del_slice(self, id):
        found = False
        for idx, slice in enumerate(self.slices):
            if slice["id"] == id:
                index = idx
                found = True
                del self.slices[idx]
                if id == 1:
                    slice1.free()
                elif id == 2:
                    slice2.free()
                #else id == 3:
                #    slice3.free()
        
        return found

    def get_all_slices(self):
        return self.slices

    def exist_value(self,value):
        found=False
        for idx, slice in enumerate(self.slices):
            if slice["nep_vue"] == value:
               found=True
        return found

    def exist_slice(self,id):
        found= False
        for idx, slice in enumerate(self.slices):
            if slice["id"] == id:
                found = True
        return found

    def get_slice(self, id):
        
        for idx, slice in enumerate(self.slices):
            if slice["id"] == id:
                sli_get={}
                sli_get["id"]=slice["id"]
                sli_get["rs_name"]=slice["rs_name"]
                sli_get["nep_vbs"]=slice["nep_vbs"]
                sli_get["nep_vue"]=slice["nep_vue"]
                sli_get["channelbw_min"]=slice["channelbw_min"]
                sli_get["channelbw_max"]=slice["channelbw_max"]
                sli_get["sharingpool"]=slice["sharingpool"]
                sli_get["chairpolicy"]=slice["chairpolicy"]
                sli_get["chairminratio"]=slice["chairminratio"]
                sli_get["chairmaxratio"]=slice["chairmaxratio"]
                sli_get["chairavgint"]=slice["chairavgint"]
                
        return json.dumps(sli_get)
    def numero(self):
        uno=len(self.slices)
        return uno     
    def contador(self):
        cont=False
        count=0
                
        if  len(self.slices) == 2:
            for idx, slice in enumerate(self.slices):
                if slice["sharingpool"]=="nonshared":
                    count=count+1
                    if count == 2:
                        cont=True
                    else:
                        cont=False
        return cont

        
    
    def update_key(self,key,value,id):
       same=False   
       
       for idx, slice in enumerate(self.slices):
           if slice["id"] == id:
               index=idx
               if self.slices[index][key] == value:
                   same=True
               else:
                    same=False
                    self.slices[index][key] = value
       return same


    def json_list(self):
        return json.dumps(self.slices)

# This class receives a hydra_client, which interacts with the Hydra-Server,
#       a xmlrpclib.ServerProxy, which interacts with the VBS side,
#       and a xmlrpclib.ServerProxy, which interacts with the UE side.
# Use the methods to configure both the client and ue at the same time.

class Slice:
    def __init__(self, id, hydra, client, ue):
        self.slice_id = id
        self.hydra = hydra
        self.client = client
        self.ue = ue
        self.freqtx = 0.0
        self.freqrx = 0.0
        self.bw = 0.0

    def free(self):
        self.hydra.free_resources()

    def allocate_tx(self, freq, bandwidth, gain, h_id):

        # Configure TX freq for slice
        print("Configure TX")
        spectrum_conf = hydra.rx_configuration(freq, bandwidth, False) 
        print("Spectrum Configuration")
        ret = self.hydra.request_tx_resources( spectrum_conf )

        if h_id == 1:
            # self.client.set_mul(gain)
            print "mul(gain)"
        elif h_id == 2:
            # self.client.set_mul2(gain)
            print "mul2(gain)"
        else:
            print("ERROR: Unknown Hydra Client ID")

        if (ret < 0):
            print "Error allocating HYDRA TX resources: freq: %f, bandwidth %f" % (freq, bandwidth)
            return -1

        #  Configure the RX freq for UE (to receive from the slice)
        self.ue.set_freqrx(freq)
        self.ue.set_vr1offset(0)
        self.ue.set_vr2offset(0)
        self.ue.set_samp_rate(bandwidth)

        if (self.ue.get_freqrx() != freq or self.ue.get_samp_rate() != bandwidth):
            print "Error allocating UE RX resources: freq: %f, bandwidth %f" % (freq, bandwidth)
            return -1

        self.freqtx = freq
        self.bw = bandwidth
        return 0

    def allocate_rx(self, freq, bandwidth):
        # Configure RX freq for slice
        spectrum_conf = hydra.rx_configuration(freq, bandwidth, False)
        ret = self.hydra.request_rx_resources( spectrum_conf )

        if (ret < 0):
            print "Error allocating RX resources: freq: %f, bandwidth %f" % (freq, bandwidth)

        #  Configure the TX freq for UE (to transmitt to the slice)
        self.ue.set_freqtx(freq)
        self.ue.set_vr1offset(0)
        self.ue.set_vr2offset(0)
        self.ue.set_samp_rate(bandwidth)

        if (self.ue.get_freqtx() != freq or self.ue.get_samp_rate() != bandwidth):
            print "Error allocating UE TX resources: freq: %f, bandwidth %f" % (freq, bandwidth)
            return -1

        self.freqrx = freq
        self.bw = bandwidth
        return 0

    
def create(slices,result,mf):
    if mf==0 or mf==1:#Add or Modify slice (When init mf=0)
                
        freqtx=1.43e9 #Canviar pel WINS_5G a 2.43e9
        freqrx=1.43e9 + 3e6 #Canviar pel WINS_5G a 2.43e9 +3e6
        ## IMPORTANT: The script ansible_hydra_client_2tx_2rx already allocated resources for transmission and reception
        ##            These resources are under the use of clients ID 1, and ID 2. The trick of this script is to connect
        ##            with the server using the same ID (1 and 2), and them releasing the resources allocated.
        ##            We can then allocate new resources from this python without impacting the slices.
        
        #Start Hydra Clients    
        # We put the IP of the machine executing this script (This is for the server updates)
        # hydra1 = hydra.hydra_client("147.83.105.229", 5000, 1, True)
        hydra1 = hydra.hydra_client(vbs, 5000, 1, True)
        # hydra2 = hydra.hydra_client("147.83.105.229", 5000, 2, True)
        hydra2 = hydra.hydra_client(vbs, 5000, 2, True)
        
        #Start VUE Control Connections 
        # We put the IP of the machine running the VUE (this is for the RX updates)
        #vue1 = xmlrpclib.ServerProxy("http://147.83.105.145:8080")
        vue1 = xmlrpclib.ServerProxy("http://vue1:8080")
        vue2 = xmlrpclib.ServerProxy("http://vue2:8080") 
        vue3 = xmlrpclib.ServerProxy("http://vue3:8080") 

        #Start VBS Control Connection
        # We put the IP of the machine running the client (this is for the client updates, mul, mul1,...)
        client = xmlrpclib.ServerProxy("http://vbs:8080")

        # if hydra1.check_connection(3) == "":
        #    print("hydra1 could not connect to server")
        #    sys.exit(1)
        # if hydra2.check_connection(3) == "":
        #    print("hydra2 could not connect to server")
        #    sys.exit(1)

        if result == "init":
            print "Initialising with default values"
            
            logging.info("VUE#1 control connection established")
            logging.info("VUE#2 control connection established")
            logging.info("VUE#3 control connection established")
            
            logging.info("VBS control connection established")    

            logging.info("Hydra client 1 connected to server")
            logging.info("Hydra client 2 connected to server")        
        
        #   slice1 = Slice(1, hydra1, client, ue1) #"non-shared"
        #   slice2 = Slice(2, hydra2, client, ue2) #"shared"
        #   slice3 = Slice(3, hydra2, client, ue3) #"shared"
        
        #   slice1.allocate_tx(freqtx- 500e3, 400e3, 0.04, 1)
        #   slice1.allocate_rx(freqrx - 500e3, 400e3)
        #   slice2.allocate_tx(freqtx + 500e3, 200e3, 0.04, 2)
        #   slice2.allocate_rx(freqrx + 500e3, 200e3)
        #   slice3.allocate_tx(freqtx + 500e3, 200e3, 0.04, 2)
        #   slice3.allocate_rx(freqrx + 500e3, 200e3)   
        else:
            print "Slice counter:"
            current=slices.numero()
            print current
            global contshared
            global contnonshared
            y=json.loads(result)
            
            s=y['sharingpool']
            if mf==0:#Add new slice 
                if s == "shared":
                    if contshared < 2 or (contshared==2 and contnonshared==0):
                        contshared= contshared+1 #S'ha de decrementar quan s'esborra la slice !!!
                        print "contshared"
                        print contshared
                    else:
                        print "ERROR: creation of a shared slice is not possible."
                else:
                    if contnonshared <1 or (contnonshared==1 and contshared==0):
                        contnonshared=contnonshared+1 #S'ha de decrementar quan s'esborra la slice !!!
                        print "contador non shared"
                        print contnonshared
                    else: 
                        print "ERROR: creation of a non-shared slice is not possible."
                x=y['channelbw_min']
                
            elif mf==1:#Modify slice 
                x=y['channelbw_max']
            
            bw=float(x)
            slice_id=y['id']
            ID=int(slice_id) 
            if ID == 1:  
                print "hola 1"   
            elif ID == 2:
                print "hola 2"
            elif ID == 3:
                print "hola 3"
            else:
                print("Slice ID not possible")
                sys.exit(1)

            slice_vue=y['nep_vue']

            if (current-mf)==0:
               if s == "shared":
                   slice1 = Slice (ID, hydra2, client, slice_vue)
                   slice1.allocate_tx(freqtx + 500e3,bw,0.05,2)
                   slice1.allocate_rx(freqrx + 500e3,bw)
               else:
                   slice1 = Slice (ID, hydra1, client, slice_vue)
                   slice1.allocate_tx(freqtx - 500e3,bw,0.05,1)
                   slice1.allocate_rx(freqrx - 500e3,bw)

            if (current-mf)==1:
               if (s == "shared"):
                   slice2 = Slice (ID, hydra2, client, slice_vue)
                   slice2.allocate_tx(freqtx + 500e3,bw,0.05,2)
                   slice2.allocate_rx(freqrx + 500e3,bw)
               else:
                   slice2 = Slice (ID, hydra1, client, slice_vue)
                   slice2.allocate_tx(freqtx - 500e3,bw,0.05,1)
                   slice2.allocate_rx(freqrx - 500e3,bw)

            if (current-mf)==2:
               if (s == "shared") and (contshared == 2):
                   slice3 = Slice (ID, hydra2, client, slice_vue)
                   slice3.allocate_tx(freqtx + 500e3,bw,0.05,2)
                   slice3.allocate_rx(freqrx + 500e3,bw)
               else:
                   slice3 = Slice (ID, hydra1, client, slice_vue)
                   slice3.allocate_tx(freqtx - 500e3,bw,0.05,1)
                   slice3.allocate_rx(freqrx - 500e3,bw)

    elif mf==-1:#Delete slice 
        y=json.loads(result)
        s=y['sharingpool']
        if s == "shared":
            #if(contshared==3):
            #   si la slice que esborro esta a hydra 2, la que hi ha a hydra1 ha de moure s a hydra2 **************
            contshared= contshared-1 #S'ha de decrementar quan s'esborra la slice !!!
            print "Decrease contshared to"
            print contshared
        else:
            #if(contnonshared==2):
            #   si la slice que esborro esta a hydra1, la que hi ha a hydra2 s ha de moure a hydra1 **************
            contnonshared=contnonshared-1 #S ha de decrementar quan s esborra la slice !!!
            print "Decrease contador non-shared to"
            print contnonshared
