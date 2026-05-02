#!/usr/bin/env python3


# DCOL_Encoder
# A simple class for encoding DCOL packet.

from DCOL_Decls import *
from binascii import hexlify, unhexlify
import sys
from time import sleep
from pprint import pprint

class DCOL_Encode:
    def encode(self, packet_Id: int, data):
        packet = bytearray()
        #        print "packet start"
        #        print hexlify(packet)
        packet.append(STX)
        #        print "packet stx"
        #        print hexlify(packet)
        packet.append(0)  # Status Byte
        packet.append(packet_Id)
        packet.append(len(data))

        if len(data):
            for b in data:
                packet.append(b)
        #                print "packet",
        #                print hexlify(packet)

        Checksum = 0
        for i in range(TrimComm_First_Checksum_Location, len(packet)):
            Checksum += packet[i]

        Checksum = Checksum % 256
        packet.append(Checksum)
        packet.append(ETX)
        #        print "packet"
        sys.stderr.buffer.write(hexlify(packet))
        return packet


if __name__ == "__main__":
    import sys

    Encode = DCOL_Encode()

    #   print hexlify(Encode.encode(int(sys.argv[1],16),sys.argv[2]))
    if len(sys.argv) == 3:
        hex_string=sys.argv[2]
        hex_string=hex_string.replace(" ", "")
#        pprint(hex_string)
        hex_bytes=unhexlify(hex_string)
#        print(hex_bytes)
        sys.stdout.buffer.write(Encode.encode(int(sys.argv[1], 16), hex_bytes))
    else:
        sys.stdout.buffer.write(Encode.encode(int(sys.argv[1], 16), b''))
    sleep(5)
