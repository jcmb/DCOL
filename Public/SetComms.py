import DCOL

# Documentation Source: 4000  RSR-232 manual 2-71

from struct import *
from binascii import hexlify
from ENUM import enum
from DCOL_Decls import *

TSet_Type = (
    'Set Baud',
    'Set Modem Init string'); # This one is not documented in the 4000 Manual

TSetComms_Parity = (
    'None',
    'Odd',
    'Even',
    'Unknown');

TSetComms_Flow_Control = (
    'None',
    'XonXoff',
    'CTS Handshaking',
    'CTS FlowControl', #not in 4000 manual, since it only did the handshaking
    'Flow Control Unknown');

class SetComms (DCOL.Dcol) :
    def __init__ (self):
        self.Port = 0
        self.Set_Type  = 0 #: TSet_Type;
        self.BAUD_RATE = 0 #: CARDINAl;
        self.DATA_BITS = 0 #: BYTE;
        self.PARITY    = 0 #: TSetComms_Parity;
        self.STOP_BITS = 0 #: BYTE;
        self.FLOW_CONTROL = 0 #: TSetComms_Flow_Control;
        self.CTS_DELAY = 0 # : BYTE;
        self.Modem_Init_Str = ""


    def decode(self,data,internal=False):
        if data[0] == 0xFF :
            self.Set_Type=1;
            del data[0]
            unpacked=unpack(str(len(data))+'s',str(data))
            self.Modem_Init_Str = unpacked[0]
        else :
            self.Set_Type=0;
#            print len(data)
#            print hexlify (data)

            unpacked=unpack('> B L B B B B B',str(data))
            self.Port = unpacked[0]
            self.BAUD_RATE = unpacked[1]
            self.DATA_BITS = unpacked[2]
            self.PARITY    = unpacked[3]
            self.STOP_BITS = unpacked[4]
            self.FLOW_CONTROL = unpacked[5]
            self.CTS_DELAY = unpacked[6]/10

        return DCOL.Got_Packet

    def dump(self,Dump_Level):

        if Dump_Level >= Dump_Summary :
            if self.Set_Type ==1 :
                print((" Modem Init String: {}".format(
                    self.Modem_Init_Str
                    )));
            else :
                print((" Port: {}  Baud: {}  Data: {}  Parity: {}  Stop: {}\n Flow Control: {} Cts Delay {:.1f}".format(
                self.Port,
                self.BAUD_RATE,
                self.DATA_BITS,
                TSetComms_Parity[self.PARITY],
                self.STOP_BITS,
                TSetComms_Flow_Control[self.FLOW_CONTROL],
                self.CTS_DELAY
                )));
