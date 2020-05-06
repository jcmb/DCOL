import DCOL

# Documentation Source: CMR Paper

from struct import *
from binascii import hexlify
from ENUM import enum
from DCOL_Decls import *

TSubtype_Names={}
TSubtype_Names[0]="Observables"
TSubtype_Names[1]="GPS Time"
TSubtype_Names[28]="ITRF Offset"

class CMRGlonass (DCOL.Dcol) :
    def __init__ (self):
        self.message_type=None
        self.ITRF_Offset_x=None
        self.ITRF_Offset_y=None
        self.ITRF_Offset_z=None

        self.GPS_Week=None
        self.GPS_Word_Of_Week=None
        self.GSP_Data_Bits_Known=None
        self.GSP_Data_Bits_Signal=None

        self.GLN_SVs=None
        pass



    def decode(self,data,internal=False):
      self.message_type=data[0]
      del data[0:1] # Remove Sub Type
      if self.message_type==0:  # Observables
        self.GLN_SVs=(len(data)-8)/15

      if self.message_type==1:  # Time Message
          unpacked = unpack('>B B H L L' ,data)
          del data[0:calcsize('>B B H L L')]

          self.GPS_Week=unpacked[0]
          self.GPS_Week<<=4
          self.GPS_Week|=unpacked[1]>>4
          self.GPS_Word_Of_Week=unpacked[1] & 0x0F
          self.GPS_Word_Of_Week<<=16
          self.GPS_Word_Of_Week|=unpacked[2]
          self.GSP_Data_Bits_Known=unpacked[3]
          self.GSP_Data_Bits_Signal=unpacked[4]

      if self.message_type==28:  # ITRF Offset Message
          unpacked = unpack('>B h h h' ,data)
          del data[0:calcsize('>B h h h')]
          self.ITRF_Offset_x=unpacked[0]
          self.ITRF_Offset_y=unpacked[1]
          self.ITRF_Offset_z=unpacked[2]


      return DCOL.Got_Packet

    def dump(self,Dump_Level):

        if Dump_Level >= Dump_Summary :
           if self.message_type in TSubtype_Names:
             print("  SubType: {} ({})  ".format(TSubtype_Names[self.message_type],self.message_type))
           else:
             print("  Unknown SubType: {}:  ".format(self.message_type))
           if self.message_type==0 :
              print("    GLN SV's: {}".format(self.GLN_SVs))

           if self.message_type==1 :
              print("    GPS Week: {} GPS_Word_Of_Week: {} Seconds of week: {}".format(self.GPS_Week,self.GPS_Word_Of_Week,self.GPS_Word_Of_Week*0.6))
           if self.message_type==28 :
              print("    ITRF_Offset_x: {} ITRF_Offset_y: {} ITRF_Offset_z: {}".format(self.ITRF_Offset_x,self.ITRF_Offset_y,self.ITRF_Offset_z))

