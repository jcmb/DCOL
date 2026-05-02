import DCOL

# Documentation Source: 4000 RS-232 Manual

from struct import *
from binascii import hexlify
from ENUM import enum
from DCOL_Decls import *
from pprint import pprint


class RetTime (DCOL.Dcol) :
    def __init__ (self):
        self.Subtype =0;
        self.Time=0
        self.Week_Number=0
        self.UTC_Offset=0
        self.Time_Offset=0
        self.Time_Mode=""

        self.Uptime=0
#        print "in recserial init"



    def decode(self,data,internal=False):
        if len (data) == 0x14:
            unpacked = unpack('>7s 4s 2s 4s 3s', data)
            del data[0:calcsize('>7s 4s 2s 4s 3s')]
            self.Subtype =0
            self.Time=unpacked[0].decode("ascii")
            self.Week_Number=unpacked[1].decode("ascii")
            self.UTC_Offset=unpacked[2].decode("ascii")
            self.Time_Offset=unpacked[3].decode("ascii")
            self.Time_Mode=unpacked[4].decode("ascii")
        elif len (data) == 0x4:
            self.Subtype =1;
            unpacked = unpack('>L' ,data)
            self.Uptime=unpacked[0]
        else :
           print("RetTime: Unknown Subtype")

        return DCOL.Got_Packet

    def dump(self,Dump_Level):

        if Dump_Level >= Dump_ID :
            print((" Subtype: {}".format(self.Subtype)))

        if Dump_Level >= Dump_Summary :
            if self.Subtype==0:
                print((" Week : {}  Time: {} UTC Offset: {}  ".format(self.Week_Number, self.Time, self.UTC_Offset)))
                if Dump_Level >= Dump_Verbose :
                    print((" Time Offset: {}  Time Mode: {}".format(self.Time_Offset,self.Time_Mode)))
            else:
                print((" Uptime : {} ".format(self.Uptime)))


