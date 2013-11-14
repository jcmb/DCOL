import DCOL

# Documentation Source: 4000 RS-232 Manual, Upto Flag

from struct import *
from binascii import hexlify
from ENUM import enum
from DCOL_Decls import *

TMessage_Names = (
   'Power out the Port',
   'Positive Slope (Event and PPS)',
   'Negative Slope (Event and PPS)',
   'Slope Swap (Event for Land Seismic)',
   'Vib truck output (triggered by event for Land Seismic)',
   'RTCM BINARY Corrections INPUT',
   'RTCM ASCII Corrections',
   'RTCM AUXILIARY Corrections',
   'RTCM BINARY Corrections',
   'RTCM ASCII Corrections Printout',
   'Position Calculation ASCII',
   'Position Calculation BINARY',
   'Raw Measurements ASCII',
   'Raw Measurements BINARY',
   'Ephem., ION, UTC ASCII',
   'Ephem., ION, UTC BINARY',
   'Position Statistics ASCII',
   'Position Statistics BINARY',
   'Navigation Calculations ASCII',
   'Navigation Display Unit ASCII',
   'Compact Measurement Record 1',
   'Raw L1 Phase Message',
   'Compact Measurement Record 2',
   'Compact Measurement Record 2 INPUT',
   'PPS ASCII Time Tag',
   'NMEA WPL (available only after NP version 5.60) (was GXP',
   'NMEA GGA',
   'NMEA GLL',
   'NMEA VTG',
   'NMEA ZDA',
   'NMEA PTNL TSS',
   'NMEA PTNL TSN',
   'NMEA BWC',
   'NMEA XTE',
   'NMEA ALM',
   'NMEA GSA',
   'NMEA GSV',
   'NMEA RMB',
   'NMEA RMC',
   'NMEA PTNL DOP',
   'Position Calculations type 2 (expanded precision) ASCII',
   'Position Calculations type 2 (expanded precision) Binary',
   'Navigation Calculations type 2 (expanded precision) ASCII',
   'NMEA-0183 GRS',
   'NMEA-0183 GST',
   'NMEA-0183 GBS',
   'Local coordinates',
   'Real-Time Survey Data',
   'NMEA GGK',
   '4700, 4800, 5x00 Series and MS Series receivers: NMEA PJK. 4600LS receivers: NMEA GST (Added 4600LS: NAV 2.6).',
   'WAAS satellite corrections control.',
   '(reserved)',
   'NMEA ADV at 1 message / 10 seconds (0.1 Hz).',
   'BINEX streamed output',
   'NMEA PTNL PJT',
   'NMEA PTNL VGK',
   'NMEA PTNL VHD',
   'NMEA GGK_SYNC',
   'NMEA AVR',
   'NMEA ROT',
   'NMEA HDT',
   'NMEA BPQ',
   'NMEA DG',
   'NMEA DP (Fugro Dynamic Positioning)',
   'NMEA GNS',
   'NMEA DTM',
   'NMEA LLQ'
   )

TCMR_Names=(
   'CMR+',
   'CMR MB',
   'CMR',
   'CMR_XT',
   'CMR_XT_MB_HS',
   'CMRx2401'
   )

class CommOut (DCOL.Dcol) :
    def __init__ (self):
        self.Port_Number=-1
        self.On_Off=False
        self.Message_Type=-1
        self.Epoch_Rate=0
        self.Flags1=None
        self.Flags2=None
        self.Extras0=None
        self.Extras1=None
        self.Extras2=None
#        print "in recserial init"



    def decode(self,data,internal=False):
        unpacked = unpack_from('>B B B H' ,str(data))
        del data[0:calcsize('> B B B H')]
        self.Port_Number=unpacked[0]
        self.On_Off=unpacked[1]
        self.Message_Type=unpacked[2]
        self.Epoch_Rate=unpacked[3]

        self.Flags1=None
        self.Flags2=None
        self.Extras0=None
        self.Extras1=None
        self.Extras2=None

        if data:
           unpacked = unpack_from('>B' ,str(data))
           del data[0:calcsize('> B')]
           self.Flags1=unpacked[0]

        if data:
           unpacked = unpack_from('>B' ,str(data))
           del data[0:calcsize('> B')]
           self.Flags2=unpacked[0]

        if data:
           unpacked = unpack_from('>B' ,str(data))
           del data[0:calcsize('> B')]
           self.Extras0=unpacked[0]

        if data:
           unpacked = unpack_from('>B' ,str(data))
           del data[0:calcsize('> B')]
           self.Extras1=unpacked[0]

        if data:
           unpacked = unpack_from('>B' ,str(data))
           del data[0:calcsize('> B')]
           self.Extras2=unpacked[0]

        return DCOL.Got_Packet

    def dump(self,Dump_Level):

        display_flags=True
        display_epoch=True

        if Dump_Level >= Dump_Summary :
            print " Port: {}  Name: {}".format(self.Port_Number, TPort_Names[self.Port_Number-1])
            print " Message Type: {}  Name : {}".format (self.Message_Type,TMessage_Names[self.Message_Type])
            if self.Message_Type == 0 :
               display_flags=False
               display_epoch=False
               if self.On_Off == 5 :
                  print " Power Output: On"
               else:
                  print " Power Output: Off"
            elif self.Message_Type == 22 :
               if self.On_Off == 0 :
                  print " CMR Output: Off"
                  display_flags=False
                  display_epoch=False
               else:
                  print " CMR Output: On "
                  if (self.Flags2 == None) or (self.Flags2 and Bit0 == 0) : # Normal CMR Output
                     print " CMR Type: {}".format(TCMR_Names[self.Flags1])
                  else:
                     print " CMR Type: SIB and Version "

            else :
               print " On/Off: {}".format(self.On_Off)

            if display_epoch:
               print " Epoch Rate: {}".format(self.Epoch_Rate)

            if display_flags:
               print " Flags1: {} Flags2: {}".format(self.Flags1,self.Flags2)
               print " Extra0: {} Extra1: {} Extra2: {}".format(self.Extras0,self.Extras1,self.Extras2)

