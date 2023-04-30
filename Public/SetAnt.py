import DCOL

# Documentation Source: 4000 RS-232 Manual

from struct import *
from binascii import hexlify
from ENUM import enum
from DCOL_Decls import *



class SetAnt (DCOL.Dcol) :
    def __init__ (self):
        self.Antenna_TYPE   =""
        self.Antenna_SERIAL ="";
#        print "in recserial init"



    def decode(self,data,internal=False):
        unpacked = unpack('>2s 8s',str(data))
        self.Antenna_TYPE   = unpacked[0]
        self.Antenna_SERIAL = unpacked[1]

        return DCOL.Got_Packet

    def dump(self,Dump_Level):

        if Dump_Level >= Dump_Summary :
            print((" ANTENNA_TYPE: {}  ANTENNA_SERIAL: {}".format(self.Antenna_TYPE, self.Antenna_SERIAL)))

