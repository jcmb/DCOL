import DCOL

# Documentation Source: Series 4000 RS-232 Interface Manual 2-7

from struct import *
from binascii import hexlify
from ENUM import enum
from DCOL_Decls import *

TRetStat1_Pos_Type= enum(
   'Old Position',
   'clock only',
   'height only',
   'height and clock fixed',
   'Two D height',
   'Three D',
   'INS',
   'Three D Wide Area');

TRetStat1_Status = (
    'Session not started',
    'waiting for start time',
    'waiting for sv to reach mask',
    'presurvey positioning',
    'one cycle delay as meas are unsynced',
    'logging data to the memory board',
    'completed a session since power up',
    'Data storage supended');

Numbers = enum('ZERO', 'ONE', 'TWO')

class RetStat1 (DCOL.Dcol) :
    def __init__ (self):
        self.MEASUREMENT_Type  = TRetStat1_Pos_Type;
        self.New_POSITION = False
        self.Number_SVS_LOCKED = 0;
        self.Number_MEAS_TO_GO = 0;
        self.BATTERY_REMAINING = 0;
        self.HOURS_OF_MEM      = 0.0
        self.STATUS_OF_SURVEY  = TRetStat1_Status;
        self.STATUS_OF_RECVR   = ''
        self.L2_CHANNELS_OPER  = 0

    def decode(self,data,internal=False):
#        print "in restat decode, data length: " + str(len(data))
#        print "data: " +hexlify(data);
#        print TRetStat1_Pos_Type
        unpacked = unpack('>c c 2s 3s 3s 4s c 4s 2s',str(data))
#        print unpacked
        b = ord(unpacked[0])-ord('0')
        self.MEASUREMENT_Type = TRetStat1_Pos_Type.reverse_mapping[b]
        self.New_POSITION = unpacked[1]== "N"
        self.Number_SVS_LOCKED = int(unpacked[2]);
#        print "SVs: " + str (self.Number_SVS_LOCKED);
        self.Number_MEAS_TO_GO = int(unpacked[3]);
#        print "To  go: " + str (self.Number_MEAS_TO_GO)
        self.BATTERY_REMAINING=float(unpacked[4]);
        self.HOURS_OF_MEM=float(unpacked[5]);
#        print "Hour: " + str(self.HOURS_OF_MEM);
        self.STATUS_OF_SURVEY = TRetStat1_Status[7];

        if unpacked[6] == "S" :
            self.STATUS_OF_SURVEY = TRetStat1_Status.reverse_mapping[7]
        else:
            b = ord(unpacked[6])-ord('0')
            self.STATUS_OF_SURVEY = self.STATUS_OF_SURVEY = TRetStat1_Status[b]

#        print self.STATUS_OF_SURVEY;
        self.STATUS_OF_RECVR=unpacked[7];
        self.L2_CHANNELS_OPER=int(unpacked[8])
#        print self.L2_CHANNELS_OPER
        return DCOL.Got_Packet

    def dump(self,Dump_Level):

        if Dump_Level >= Dump_Summary :
            print ' SV\'s: {:<21d} Battery %: {:<15.1f} Reciever Status: {:<10s} Position Type: {}{}'.format(self.Number_SVS_LOCKED,self.BATTERY_REMAINING,self.STATUS_OF_RECVR, "" if self.New_POSITION else "OLD ",self.MEASUREMENT_Type)

        if Dump_Level >= Dump_Full :
            print ' Measurements to go: {:<7d} Hours of Memory: {:<9.1f} L2 Channels: {:<14d} Status: {}'.format(self.Number_MEAS_TO_GO,self.HOURS_OF_MEM,self.L2_CHANNELS_OPER,self.STATUS_OF_SURVEY)

