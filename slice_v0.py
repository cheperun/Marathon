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
            self.client.set_mul(gain)
        elif h_id == 2:
            self.client.set_mul2(gain)
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
    if mf==0 or mf==1:#Add or Modify slice 
                
        freqtx=1.43e9 #Canviar pel WINS_5G a 2.43e9
        freqrx=1.43e9 + 3e6 #Canviar pel WINS_5G a 2.43e9 +3e6
        
        if result == "init":
            print "Initialising with default values"
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
                #Start Hydra Clients    
                # We put the IP of the machine executing this script (This is for the server updates)
                #hydra1 = hydra.hydra_client("147.83.105.233", 5000, 1, True)
                hydra1 = hydra.hydra_client(vbs, 5000, 1, True)
                #hydra2 = hydra.hydra_client("147.83.105.233", 5000, 2, True)
                hydra2 = hydra.hydra_client(vbs, 5000, 2, True)
                
                #Start VUE Connections 
                # We put the IP of the machine running the UE (this is for the RX updates)
                #ue1 = xmlrpclib.ServerProxy("http://147.83.105.145:8080")
                ue1 = xmlrpclib.ServerProxy("http://vue1:8080")
                ue2 = xmlrpclib.ServerProxy("http://vue2:8080") 
                ue3 = xmlrpclib.ServerProxy("http://vue3:8080") 
                
                #Start VBS Connection
                # We put the IP of the machine running the client (this is for the client updates, mul, mul1,...)
                client = xmlrpclib.ServerProxy("http://vbs:8080")
                    
                # if hydra1.check_connection(3) == "":
                #    print("hydra1 could not connect to server")
                #    sys.exit(1)
                #if hydra2.check_connection(3) == "":
                #    print("hydra2 could not connect to server")
                #    sys.exit(1)

                logging.info("Hydra client 1 connected to server")
                logging.info("Hydra client 2 connected to server")
                logging.info("Hydra client 3 connected to server")

                logging.info("VBS connection established")

                logging.info("VUE#1 connection established")
                logging.info("VUE#2 connection established")
                logging.info("VUE#3 connection established")
    
            elif mf==1:#Modify slice 
                x=y['channelbw_max']
            
            bw=float(x)
            if y['id']=="1":  
                print "hola 1" 
                ID = 1   
            elif y['id']=="2":
                print "hola 2"
                ID = 2
            elif y['id']=="3":
                print "hola 3"
                ID = 3
            else:
                print("Slice ID not possible")
                #sys.exit(1)

            #if (current-mf)=0:
            #   if s == "shared":
            #       slice1 = Slice (ID, hydra2, client, nep_vue)
            #       slice1.allocate_tx(freqtx + 500e3,bw,0.05,2)
            #       slice1.allocate_rx(freqrx + 500e3,bw)
            #   else:
            #       slice1 = Slice (ID, hydra1, client, nep_vue)
            #       slice1.allocate_tx(freqtx - 500e3,bw,0.05,1)
            #       slice1.allocate_rx(freqrx - 500e3,bw)
            
            #if (current-mf)=1:
            #   if (s == "shared") or (slice1.sharingpool == 'non-sharing'):
            #       slice2 = Slice (ID, hydra2, client, nep_vue)
            #       slice2.allocate_tx(freqtx + 500e3,bw,0.05,2)
            #       slice2.allocate_rx(freqrx + 500e3,bw)
            #   else:
            #       slice2 = Slice (ID, hydra1, client, nep_vue)
            #       slice2.allocate_tx(freqtx - 500e3,bw,0.05,1)
            #       slice2.allocate_rx(freqrx - 500e3,bw)

            #if (current-mf)=2:
            #   if (slice1.sharingpool == 'non-sharing') or (slice2.sharingpool == 'non-sharing'):
            #       slice3 = Slice (ID, hydra2, client, nep_vue)
            #       slice3.allocate_tx(freqtx + 500e3,bw,0.05,2)
            #       slice3.allocate_rx(freqrx + 500e3,bw)
            #   else:
            #       slice3 = Slice (ID, hydra1, client, nep_vue)
            #       slice3.allocate_tx(freqtx - 500e3,bw,0.05,1)
            #       slice3.allocate_rx(freqrx - 500e3,bw)

        
        ## IMPORTANT: The script ansible_hydra_client_2tx_2rx already allocated resources for transmission and reception
        ##            These resources are under the use of clients ID 1, and ID 2. The trick of this script is to connect
        ##            with the server using the same ID (1 and 2), and them releasing the resources allocated.
        ##            We can then allocate new resources from this python without impacting the slices. 
        
    elif mf==-1:#Delete slice 
        y=json.loads(result)
        s=y['sharingpool']
        if s == "shared":
            contshared= contshared-1 #S'ha de decrementar quan s'esborra la slice !!!
            print "Decrease contshared to"
            print contshared
        else:
            contnonshared=contnonshared-1 #S'ha de decrementar quan s'esborra la slice !!!
            print "Decrease contador non-shared to"
            print contnonshared
