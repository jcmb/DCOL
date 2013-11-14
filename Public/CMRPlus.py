import DCOL

# Documentation Source: CMR Paper

from struct import *
from binascii import hexlify
from ENUM import enum
from DCOL_Decls import *



class CMRPlus (DCOL.Dcol) :
    def __init__ (self):
        pass



    def decode(self,data,internal=False):
        unpacked=unpack_from('> B B B',str(data))
        self.station_ID=unpacked[0]
        self.Page_Index=unpacked[1]
        self.Max_Page_Index=unpacked[2]
        return DCOL.Got_Packet

    def dump(self,Dump_Level):

        if Dump_Level >= Dump_Summary :
            print "  ID: {},  Page: {}, Max Page: {}".format(
              self.station_ID,
              self.Page_Index,
              self.Max_Page_Index)

