import DCOL

# Documentation Source: BD970 Manual

from struct import *
from binascii import hexlify
from ENUM import enum
from DCOL_Decls import *



class RetBreak (DCOL.Dcol) :
    def __init__ (self):
        self.breakString=""
        self.Product=""
        self.Port=""
        self.PortStatus=""
        self.Version=""
        self.Comm=""
        self.Serial=""
        self.Name=""
        self.ETHIP=""
        self.RefVer=""


    def decode(self,data,internal=False):
        self.breakString = unpack('>' + str(len(data)) + 's' ,str(data))[0]
        line=self.breakString
        (s,sep,line) = line.partition(';')
        (s,sep,self.Product)= s.partition(',')
        (s,sep,line) = line.partition(';')
        (s,sep,self.Port)= s.partition(',')
        (s,sep,line) = line.partition(';')
        (s,sep,self.PortStatus)= s.partition(',')
        (s,sep,line) = line.partition(';')
        (s,sep,self.Version)= s.partition(',')
        (s,sep,line) = line.partition(';')
        (s,sep,self.Comm)= s.partition(',')
        (s,sep,line) = line.partition(';')
        (s,sep,self.Serial)= s.partition(',')
        (s,sep,line) = line.partition(';')
        (s,sep,self.Name)= s.partition(',')
        (s,sep,line) = line.partition(';')
        (s,sep,self.ETHIP)= s.partition(',')
        (s,sep,line) = line.partition(';')
        (s,sep,self.RefVer)= s.partition(',')

        return DCOL.Got_Packet

    def dump(self,Dump_Level):

        if Dump_Level >= Dump_Summary :
            print(" Product: {}, Serial: {}, Version: {},  RefVer: {}".format (
               self.Product,
               self.Serial,
               self.Version,
               self.RefVer
               ))

            print(" Name: {}".format(
               self.Name
               ))

            print(" Port: {}   Status: {}  Comm: {}  Ethernet: {}".format(
               self.Port,
               self.PortStatus,
               self.Comm,
               self.ETHIP
               ))


        if Dump_Level >= Dump_Verbose :
            print(" {}".format(
                self.breakString
                ))


