
from utils import DynamicArray
import random
class HashTable(DynamicArray): 
    def __init__(self, size, probe=0):
        super().__init__(size)
        self.probe = probe
        self.maxfactor = 0
        if self.probe == 1:
            self.maxfactor = .5
        else:
            self.maxfactor = 1

    def hashCode(self, key):
        return key % self.get_size()
    
    def __getitem__(self, key):

        #Compute hashcode
        hashCode = self.hashCode(key)
        #Get key value pair
        keyValuePair = super().__getitem__(hashCode)
        
        #check if entry at hashcode has the key
        if keyValuePair == None:#check for empty slot, return none
            return None
        elif keyValuePair[0] == key:#if not empty, than return the value
            return keyValuePair[1]
        
        
        #Probing since hashcode is not at the key
        else:
            #linear probing
            if self.probe == 0:
                probeStep = 1
                while True:
                    probeIndex = (hashCode + probeStep) % self.get_size()#linear probing index
                    keyValuePair = super().__getitem__(probeIndex)
                    if keyValuePair == None:#check for empty slot
                        return None
                    elif keyValuePair[0] == key:
                        return keyValuePair[1]
                    probeStep += 1
            #quad probing
            elif self.probe == 1:
                probeStep = 1
                while True:
                    probeIndex = (hashCode + probeStep**2) % self.get_size()#quadratic probing index
                    keyValuePair = super().__getitem__(probeIndex)
                    if keyValuePair == None:#check for empty slot
                        return None
                    elif keyValuePair[0] == key:
                        return keyValuePair[1]
                    probeStep += 1
            #random probing     
            else:
                for i in range(1000):
                    probeStep = random.randint(1, self.get_size())#generate random number
                    probeIndex = (hashCode + probeStep) % self.get_size()#random probing index
                    keyValuePair = super().__getitem__(probeIndex)
                    if keyValuePair == None: #check for empty slot
                        return None
                    elif keyValuePair[0] == key:
                        return keyValuePair[1]
                    
    def __setitem__(self, key, value): 
        
        if self.loadfactor() >= self.maxfactor:
            self.reallocate(self.get_size()*2, self.probe) 
                   
        #first compute the hashcode
        hashCode = self.hashCode(key)
        keyValuePair = super().__getitem__(hashCode)
        
        if keyValuePair == None or keyValuePair == 'DELETED': #Is this an empty slot?
            super().__setitem__(hashCode, [key, value])#if it is, we insert the key value pair
            return
        
        elif keyValuePair[0] == key:
            super().__setitem__(hashCode, [key, value])
            return    
        
        #check if the entry at the hashcode empty?

        
        #if not, we probe
        else:
            #linear probing
            if self.probe == 0: 
                probeStep = 1
                while True:
                    probeIndex = (hashCode + probeStep) % self.get_size()
                    keyValuePair = super().__getitem__(probeIndex)
                    if keyValuePair == None or keyValuePair == 'DELETED': #is this an empty slot?
                        super().__setitem__(probeIndex, [key, value])
                        return
                    elif keyValuePair[0] == key:
                        super().__setitem__(probeIndex, [key, value])
                        return
                    probeStep += 1
            #quad probing
            elif self.probe == 1:
                probeStep = 1
                while True:
                    probeIndex = (hashCode + probeStep ** 2) % self.get_size()
                    keyValuePair = super().__getitem__(probeIndex)
                    if keyValuePair == None or keyValuePair == 'DELETED': #Is this an empty slot
                        super().__setitem__(probeIndex, [key, value])
                        return
                    elif keyValuePair[0] == key:
                        super().__setitem__(probeIndex, [key, value])
                        return
                    probeStep += 1
                    if probeStep == 50:
                        self.reallocate(self.get_size()*2, self.probe)
            #random probing     
            else:
                for i in range(1000):
                    probeStep = random.randint(1, self.get_size())#generate random number
                    probeIndex = (hashCode + probeStep) % self.get_size()#random probing index
                    keyValuePair = super().__getitem__(probeIndex)
                    if keyValuePair == None or keyValuePair == 'DELETED': #check for empty slot
                        super().__setitem__(probeIndex, [key, value])
                        return
                    elif keyValuePair[0] == key:
                        super().__setitem__(probeIndex, [key, value])
                                           
    def __delitem__(self, key):

        if self.loadfactor() >= self.maxfactor:
            self.reallocate(self.get_size()*2, self.probe) 
                
        #check if entry at the hascode
        #if entry is empty, we don't have the key in our hastable
        #if entry contains the key-value pair, we delete it
        #if not, probe
        #Compute hashcode
        hashCode = self.hashCode(key)
        keyValuePair = self.data[hashCode]
        
        #check if entry is at hashcode
        if keyValuePair == None or keyValuePair == 'DELETED':
            return
        elif keyValuePair[0] == key:
            self.data[hashCode] = 'DELETED'
            return
        else:
            #linear probing
            if self.probe == 0:
                probeStep = 1
                while True:
                    probeIndex = (hashCode + probeStep) % self.get_size()
                    keyValuePair = super().__getitem__(probeIndex)
                    if keyValuePair == None: #check for empty slot
                        return
                    elif keyValuePair[0] == key:
                        super().__setitem__(hashCode, 'DELETED')
                        return
                    probeStep += 1
            #quadratic probing
            elif self.probe == 1:
                probeStep = 1
                while True:
                    probeIndex = (hashCode + (probeStep ** 2)) % self.get_size()
                    keyValuePair = self.data[probeIndex]
                    if keyValuePair == None: #Is this an empty slot
                        return None
                    elif keyValuePair[0] == key:
                        self.data[hashCode] = 'DELETED'
                        return
                    probeStep += 1
            #random probing
            else:
                for i in range(1000):
                    probeStep = random.randint(1, self.get_size())#generate random number
                    probeIndex = (hashCode + probeStep) % self.get_size()#random probing index
                    keyValuePair = self.data[probeIndex]
                    if keyValuePair == None: #check for empty slot
                        return None
                    elif keyValuePair[0] == key:
                        super().__setitem__(hashCode, 'DELETED')
                        return
    def loadfactor(self):
        return (self.__len__())/(self.get_size())
