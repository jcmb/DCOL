import DCOL

# Documentation Source: CMR Paper

from struct import *
from binascii import hexlify
from ENUM import enum
from DCOL_Decls import *


TMotion_Names= (
   'Unknown 0',
   'Static',
   'Kinematic',
   'Unknown 3')

class CMR (DCOL.Dcol) :
   def __init__ (self):

      self.version_number=None
      self.station_ID=None
      self.message_type=None

      self.CMR=False
      self.MB=False
      self.CMRx=False
      self.Dummy=False

#Type 1 _ 2 Header
      self.Low_Base_Battery=None
      self.Low_Base_Memory=None
      self.Maxwell=None
      self.L2_Enabled=None
      self.Reserved=None
      self.Epoch_Time = None
      self.Motion_State = None
      self.Antenna_Type=None

   def decode_type_1 (self,data):
      return DCOL.Got_Packet


   def decode_type_1_2_header(self,data):
      unpacked=unpack_from('> B',str(data))
      del data[0:calcsize('> B')]

      self.Low_Base_Battery=unpacked[0]& Bit4 != 0
      self.Low_Base_Memory=unpacked[0]& Bit3 != 0
      self.Maxwell=unpacked[0]& Bit2 != 0
      self.L2_Enabled=unpacked[0]& Bit1 != 0
      self.Reserved=unpacked[0]& Bit0 != 0

      unpacked=unpack_from('> H',str(data))
      del data[0:calcsize('> H')]
      self.Epoch_Time = unpacked[0] << 2

      unpacked=unpack_from('> B',str(data))
      del data[0:calcsize('> B')]
      self.Epoch_Time |= unpacked[0] >> 6 # High 2 bytes
      self.Motion_State = (unpacked[0] & (Bit5 | Bit4))>>4

      unpacked=unpack_from('> B',str(data))
      del data[0:calcsize('> B')]
      self.Antenna_Type=unpacked[0]

   def decode(self,data,internal=False):
      unpacked=unpack_from('> B B',str(data))
      del data[0:calcsize('> B')] #Yes this is only a single byte, since byte 2 has 5 bits needed in the sub decoders

#      print "Unpacked 0 {:X}".format(unpacked[0])
      self.version_number=unpacked[0]>>5
#      print "Version Number: {:X}".format(self.version_number)
      self.station_ID=unpacked[0] & 0x1F
      self.message_type=unpacked[1]>>5

      self.CMR=self.message_type==0 or self.message_type==1 or self.message_type==2
      self.MB=self.message_type==4
      self.CMRx=self.version_number==5
      if self.CMRx:
         self.CMR=False
      self.Dummy=self.message_type==7
      self.Flags=unpacked[1] & 0x1F

      if (self.message_type == 1) or (self.message_type == 2) :
         return DCOL.Got_Packet
         self.decode_type_1_2_header(data)
         return self.decode_type_1(data)
      else :
         return DCOL.Got_Packet






   def dump(self,Dump_Level):

      if Dump_Level >= Dump_Summary :
#         print "Version Number: {:X}".format(self.version_number)
         if self.CMRx:
            print "CMRx"
            print "   Type: {}  ID: {}".format(
               self.message_type,
               self.station_ID
               )
         elif self.Dummy :
            print "Dummy CMR"
         else :
            if (self.message_type == 2) or (self.message_type==1) :
               if Dump_Level >= Dump_Summary :
                  print "Epoch_Time: {}".format(self.Epoch_Time)
                  print "Low Base Battery: {}, Low Base Memory: {}, L2 Enabled: {}".format(self.Low_Base_Battery,self.Low_Base_Memory,self.L2_Enabled)
                  print "Motion: {}, Antenna Type: {}".format(TMotion_Names[self.Motion_State],self.Antenna_Type)
               if Dump_Level >= Dump_Verbose :
                  print "Maxwell: {}, Reserved: {}".format(self.Maxwell,self.Reserved)

            if self.message_type == 1:
               pass
            elif self.message_type == 2:
               pass
            else :
               print "   Type: {}  ID: {}  Version: {}".format(
               self.message_type,
               self.station_ID,
               self.version_number);

