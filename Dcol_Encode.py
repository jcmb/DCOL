# DCOL_Encoder
# A simple class for encoding DCOL packet.

from DCOL_Decls import *
from binascii import hexlify

class Dcol_Encode:
    def encode (self, packet_Id, data) :
        packet=bytearray()
#        print "packet start"
#        print hexlify(packet)
        packet.append(STX)
#        print "packet stx"
#        print hexlify(packet)
        packet.append(0) # Status Byte
        packet.append(packet_Id)
        packet.append(len(data))

        if len(data):
            for b in data :
                packet.append(b)
#                print "packet"
#                print hexlify(packet)

        Checksum = 0;
        for i  in range (TrimComm_First_Checksum_Location,len(packet)):
             Checksum += packet[i];

        Checksum = Checksum % 256
        packet.append(Checksum)
        packet.append(ETX)
#        print "packet"
#        print hexlify(packet)

        return packet

