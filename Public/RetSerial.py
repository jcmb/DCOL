import DCOL

# Documentation Source: BD970 Manual

from struct import *
from binascii import hexlify
from ENUM import enum
from DCOL_Decls import *



class RetSerial (DCOL.Dcol) :
    def __init__ (self):
        self.RECEIVER_SERIAL ="";
        self.RECEIVER_TYPE   =""
        self.NAV_PROCESS_VER = 0.0
        self.SIG_PROCESS_VER = 0.0
        self.BOOT_ROM_VER    = 0.0
        self.ANTENNA_SERIAL  =''
        self.ANTENNA_TYPE    = '  '
        self.NUMBER_CHANNELS = 0;
        self.NUMBER_CHANNELS_L1 = 0
        self.Local_ANTENNA_SERIAL = ""
        self.BASE_ANTENNA_SERIAL  = ""
        self.BASE_ANTENNA_TYPE    = ""
        self.BASE_NGS_ANT_DESCRIPTOR = ""
        self.USABLE_CHANNELS = 0
        self.PHYSICAL_CHANNELS = 0
        self.SIMULTANEOUS_SVs = 0
        self.ANTENNA_INI_VERSION = ""
#        print "in recserial init"



    def decode(self,data,internal=False):
        unpacked = unpack('>8s 8s 5s 5s 5s 8s 2s 2s 2s 10s 31s 31s 31s H H B 5s',str(data))
        self.RECEIVER_SERIAL = unpacked[0]
        self.RECEIVER_TYPE   = unpacked[1]
        self.NAV_PROCESS_VER = float(unpacked[2])/100
        self.SIG_PROCESS_VER = float(unpacked[3])/100
        self.BOOT_ROM_VER    = float(unpacked[4])/100
        self.ANTENNA_SERIAL  = unpacked[5]
        self.ANTENNA_TYPE    = unpacked[6]
        self.NUMBER_CHANNELS = unpacked[7];
        self.NUMBER_CHANNELS_L1 = unpacked[8]
        self.Local_ANTENNA_SERIAL = unpacked[9]
        self.BASE_ANTENNA_SERIAL  = unpacked[10]
        self.BASE_ANTENNA_TYPE    = unpacked[11]
        self.BASE_NGS_ANT_DESCRIPTOR = unpacked[12]
        self.USABLE_CHANNELS = unpacked[13]
        self.PHYSICAL_CHANNELS = unpacked[14]
        self.SIMULTANEOUS_SVs = unpacked[15]
        self.ANTENNA_INI_VERSION = float(unpacked[16])/100

        return DCOL.Got_Packet

    def dump(self,Dump_Level):

        if Dump_Level >= Dump_Summary :
            print((" {} {}".format(self.RECEIVER_TYPE, self.RECEIVER_SERIAL)))
            print((" Nav Version: {:7.2f} Signal Version: {:6.2f} Boot Verison: {:7.2f}".format(self.NAV_PROCESS_VER,self.SIG_PROCESS_VER,self.BOOT_ROM_VER)))
            print((" USABLE CHANNELS: {} PHYSICAL CHANNELS: {} SIMULTANEOUS SVs: {}".format(self.USABLE_CHANNELS, self.PHYSICAL_CHANNELS, self.SIMULTANEOUS_SVs)))
            print((" ANTENNA_TYPE: {}     Local_ANTENNA_SERIAL: {}".format(self.ANTENNA_TYPE, self.Local_ANTENNA_SERIAL)))
            print((" BASE_ANTENNA_TYPE: {} BASE_ANTENNA_SERIAL: {}\n BASE_NGS_ANT_DESCRIPTOR: {}".format(self.BASE_ANTENNA_SERIAL, self.BASE_ANTENNA_TYPE, self.BASE_NGS_ANT_DESCRIPTOR)));
            print((" ANTENNA_INI_VERSION: {}".format (self.ANTENNA_INI_VERSION)))

        if Dump_Level >= Dump_Verbose :
            print((" Channels: {} L1 Channels: {}".format(self.NUMBER_CHANNELS, self.NUMBER_CHANNELS_L1)))
