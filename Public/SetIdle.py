import DCOL

# Documentation Source: 4000 RS-232 Manual

from struct import *
from binascii import hexlify
from ENUM import enum
from DCOL_Decls import *


TUse_Height_Names = (
   'No',
   'WGS-84 Height',
   'MSL Height'
   )


class SetIdle (DCOL.Dcol) :
   def __init__ (self):
      self.Epoch_Interval = None
      self.Elevation_Mask = None
      self.Pos_Type       = None
      self.Calc_Flags_1   = None
      self.PDOP           = None
      self.Calc_Flags_2   = None
      self.Use_Height     = None
      self.Height         = -1
      self.GPS_Corr_Age   = None
      self.GLN_Corr_Age   = None
      self.GAL_Corr_Age   = None
      self.BDS_Corr_Age   = None


#        print "in recserial init"



   def decode(self,data,internal=False):
      unpacked = unpack('>H B B B B B B d',str(data))
      del data[0:calcsize('> H B B B B B B d')]

      self.Epoch_Interval = unpacked[0]
      self.Elevation_Mask = unpacked[1]
      self.Pos_Type       = unpacked[2]
      self.Everest        = (unpacked[3] & Bit7 == 0)
      self.PDOP           = unpacked[4]
      self.Calc_Flags_2   = unpacked[5]
      self.Use_Height     = unpacked[6]
      self.Height         = unpacked[7]

      if data:
         unpacked = unpack('>H',str(data))
         del data[0:calcsize('> H')]
         self.GPS_Corr_Age=unpacked[0]

      if data:
         unpacked = unpack('>H',str(data))
         del data[0:calcsize('> H')]
         self.GLN_Corr_Age=unpacked[0]

      if data:
         unpacked = unpack('>H',str(data))
         del data[0:calcsize('> H')]
         self.GAL_Corr_Age=unpacked[0]

      if data:
         unpacked = unpack('>H',str(data))
         del data[0:calcsize('> H')]
         self.BDS_Corr_Age=unpacked[0]

      if (self.Calc_Flags_2 & Bit3 == 0):
         self.Epoch_Interval*=100 # Convert the Epoch interval to ms always

      return DCOL.Got_Packet

   def dump(self,Dump_Level):

      if Dump_Level >= Dump_Summary :
         print((" Epoch Interval: {}ms".format(self.Epoch_Interval)))
         print((" Elevation Mask: {} PDOP Mask: {}".format(self.Elevation_Mask,self.PDOP)))
         print((" Everest: {}  Flags 2: {:x}".format(self.Everest,self.Calc_Flags_2)))
         print((" Use Height: {}  Height: {}".format(TUse_Height_Names[self.Use_Height],self.Height)))
         print((" Corr Age:: GPS: {} GLN: {} GAL: {} BDS: {}".format(self.GPS_Corr_Age,self.GLN_Corr_Age,self.GAL_Corr_Age,self.BDS_Corr_Age)))
