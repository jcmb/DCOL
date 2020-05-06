#!/usr/bin/env python

# DCOL_Encoder
# A simple class for encoding DCOL packet.

from DCOL_Decls import *
from binascii import hexlify, unhexlify

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
#                print "packet",
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

if __name__ == "__main__":
   import sys
   Encode=Dcol_Encode()

#   print hexlify(Encode.encode(int(sys.argv[1],16),sys.argv[2]))
   print((Encode.encode(int(sys.argv[1],16),unhexlify(sys.argv[2]))))
