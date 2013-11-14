import DCOL

# Documentation Source: 4000 RS-232 Manual

from struct import *
from binascii import hexlify
from ENUM import enum
from DCOL_Decls import *



class GetTime (DCOL.Dcol) :
    def __init__ (self):
        self.Subtype_Included   =False
        self.Subtype =0;
#        print "in recserial init"



    def decode(self,data,internal=False):
        if data:
            unpacked = unpack('>B' ,str(data))
            del data[0:calcsize('> B')]
            self.Subtype_Included=True
            self.Subtype =unpacked[0]
        else:
            self.Subtype_Included=False
            self.Subtype =0;

        return DCOL.Got_Packet

    def dump(self,Dump_Level):

        if Dump_Level >= Dump_Summary :
            print " Subtype Included: {}  Subtype: {}".format(self.Subtype_Included, self.Subtype)

