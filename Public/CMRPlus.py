import DCOL

# Documentation Source: CMR Paper

from struct import *
from binascii import hexlify
from ENUM import enum
from DCOL_Decls import *
from pprint import pprint
import numpy
from decodeSCStation import decodeSCStation


class CMRPlus (DCOL.Dcol) :
    def __init__ (self):

        self.packet_data=bytearray(0)
        self.pages_seen=[]
        self.packet_data_len=None

        self.Low_Base_Battery=None
        self.Low_Base_Memory=None
        self.Maxwell=None
        self.L2_Enabled=None
        self.Reserved=None
        self.Motion_State = None
        self.Receiver_Type=None
        self.Antenna_Type=None
        self.X=None
        self.Y=None
        self.Z=None
        self.Antenna_Height=None
        self.East_Offset=None
        self.North_Offset=None
        self.Position_Accuracy=None
        self.Short_Station=None
        self.COGO_Code=None
        self.Long_Station=None
# Decoded from long station. If errLocation is None
        self.stationName=None
        self.code=None
        self.basePointQuality=None
        self.basePointType=None
        self.errLocation=None
        self.trackingDetails=None
        self.antennaType=None
        self.antennaMeasure=None
        self.protocol=None

    def decode_Plus_buffer(self,data):

        unpacked=unpack_from('> B',data)
        del data[0:calcsize('> B')]
        if unpacked[0] != 1:
            print("Invalid CMR+ 1 Subtype {}").format(unpacked[0])
            return DCOL.Invalid_Decode

        unpacked=unpack_from('> B',data)
        del data[0:calcsize('> B')]
        if unpacked[0] != 6: # Really shouldn't be invalid if we add, but the decoder will not work
            print("Invalid CMR+ Subtype 1 length {}").format(unpacked[0])
            return DCOL.Invalid_Decode


        unpacked=unpack_from('> B',data)
        del data[0:calcsize('> B')]
        self.Low_Base_Battery=unpacked[0]& Bit4 != 0
        self.Low_Base_Memory=unpacked[0]& Bit3 != 0
        self.Maxwell=unpacked[0]& Bit2 != 0
        self.L2_Enabled=unpacked[0]& Bit1 != 0

        unpacked=unpack_from('> B',data)
        del data[0:calcsize('> B')]
        self.Motion_State = (unpacked[0] & (Bit5 | Bit4))>>4

        unpacked=unpack_from('> B',data)
        del data[0:calcsize('> B')]
        self.Receiver_Type=unpacked[0]

        unpacked=unpack_from('> B',data)
        del data[0:calcsize('> B')]
        self.Antennna_Type=unpacked[0]

        unpacked=unpack_from('> B',data)
        del data[0:calcsize('> B')]

        if unpacked[0] != 2:
            print("Invalid CMR+ 2 Subtype {}".format(unpacked[0]))
            return DCOL.Invalid_Decode

        unpacked=unpack_from('> B',data)
        del data[0:calcsize('> B')]
        if unpacked[0] != 21: # Really shouldn't be invalid if we add, but the decoder will not work
            print("Invalid CMR+ Subtype 2 Subtype {}").format(unpacked[0])
            return DCOL.Invalid_Decode

        I64=numpy.int64(0)
        B=numpy.uint8(unpack_from('> B',data)[0])
        del data[0:calcsize('> B')]
        I64 = B << (32-8);

        B=numpy.uint8(unpack_from('> B',data)[0])
        del data[0:calcsize('> B')]
        I64 = I64 | (B << (32-16));

        B=numpy.uint8(unpack_from('> B',data)[0])
        del data[0:calcsize('> B')]
        I64 = I64 | (B << (32-24 ));

        B=numpy.uint8(unpack_from('> B',data)[0])
        del data[0:calcsize('> B')]
        I64 = I64 | B;

        '''
        {Here we have a 32bit signed int, based on the 32 MS bits from the data}
        {Just move this over by 2 and add the new bits}
        '''

        B=numpy.int8(unpack_from('> B',data)[0])
        #      del data[0:calcsize('> B')]  Dont delete here as we use the other parts later
        B = (B & (Bit7 | Bit6));
        B = B >> 6;
        I64 = (I64 << 2);
        I64 = I64 | B;
        if (I64 & 0x0000000200000000) != 0 :
         I64=I64-(1<<34) # Convert unsigned 32 Bit number to negative
        #         numpy.bitwise_or(I64,numpy.uint64(0xFFFFFFFC00000000)); #{Sign extend}

        self.X = I64;
        #      print self.X

        B=numpy.int8(unpack_from('> B',data)[0])
        del data[0:calcsize('> B')]
        B = (B & (~ (Bit7 | Bit6)))
        self.Antenna_Height=B<<8
        B=numpy.int8(unpack_from('> B',data)[0])
        del data[0:calcsize('> B')]
        self.Antenna_Height|=B
        #      print self.Antenna_Height

        I64=numpy.int64(0)
        B=numpy.uint8(unpack_from('> B',data)[0])
        del data[0:calcsize('> B')]
        I64 = B << (32-8);

        B=numpy.uint8(unpack_from('> B',data)[0])
        del data[0:calcsize('> B')]
        I64 = I64 | (B << (32-16));

        B=numpy.uint8(unpack_from('> B',data)[0])
        del data[0:calcsize('> B')]
        I64 = I64 | (B << (32-24 ));

        B=numpy.uint8(unpack_from('> B',data)[0])
        del data[0:calcsize('> B')]
        I64 = I64 | B;

        '''
        {Here we have a 32bit signed int, based on the 32 MS bits from the data}
        {Just move this over by 2 and add the new bits}
        '''

        B=numpy.int8(unpack_from('> B',data)[0])
        #      del data[0:calcsize('> B')]  Dont delete here as we use the other parts later
        B = (B & (Bit7 | Bit6));
        B = B >> 6;
        I64 = (I64 << 2);
        I64 = I64 | B;
        if (I64 & 0x0000000200000000) != 0 :
         I64=I64-(1<<34) # Convert unsigned 32 Bit number to negative
        #         numpy.bitwise_or(I64,numpy.uint64(0xFFFFFFFC00000000)); #{Sign extend}

        self.Y = I64;
        #      print self.Y

        B=numpy.int8(unpack_from('> B',data)[0])
        del data[0:calcsize('> B')]
        B = (B & (~ (Bit7 | Bit6)))
        self.East_Offset=numpy.uint16(B<<8)
        B=numpy.int8(unpack_from('> B',data)[0])
        del data[0:calcsize('> B')]
        self.East_Offset|=B
        #      print self.East_Offset


        I64=numpy.int64(0)
        B=numpy.uint8(unpack_from('> B',data)[0])
        del data[0:calcsize('> B')]
        I64 = B << (32-8);

        B=numpy.uint8(unpack_from('> B',data)[0])
        del data[0:calcsize('> B')]
        I64 = I64 | (B << (32-16));

        B=numpy.uint8(unpack_from('> B',data)[0])
        del data[0:calcsize('> B')]
        I64 = I64 | (B << (32-24 ));

        B=numpy.uint8(unpack_from('> B',data)[0])
        del data[0:calcsize('> B')]
        I64 = I64 | B;

        '''
        {Here we have a 32bit signed int, based on the 32 MS bits from the data}
        {Just move this over by 2 and add the new bits}
        '''

        B=numpy.int8(unpack_from('> B',data)[0])
        #      del data[0:calcsize('> B')]  Dont delete here as we use the other parts later
        B = (B & (Bit7 | Bit6));
        B = B >> 6;
        I64 = (I64 << 2);
        I64 = I64 | B;
        if (I64 & 0x0000000200000000) != 0 :
         I64=I64-(1<<34) # Convert unsigned 32 Bit number to negative
        #         numpy.bitwise_or(I64,numpy.uint64(0xFFFFFFFC00000000)); #{Sign extend}

        self.Z = I64;
        #      print self.Z

        B=numpy.int8(unpack_from('> B',data)[0])
        del data[0:calcsize('> B')]
        B = (B & (~ (Bit7 | Bit6)))
        self.North_Offset=numpy.uint16(B<<8)
        B=numpy.int8(unpack_from('> B',data)[0])
        del data[0:calcsize('> B')]
        self.North_Offset|=B
        #      print self.North_Offset

        B=numpy.uint8(unpack_from('> B',data)[0])
        del data[0:calcsize('> B')]
        B = B >> 4;
        self.Position_Accuracy=B

        unpacked=unpack_from('> B',data)
        del data[0:calcsize('> B')]
        if unpacked[0] != 3:
            print("Invalid CMR+ 3 Subtype {}").format(unpacked[0])
            return DCOL.Invalid_Decode

        Length=numpy.uint8(unpack_from('> B',data)[0])
        del data[0:calcsize('> B')]

#        if Length < 27 or Length > 76: # Really shouldn't be invalid if we add, but the decoder will not work
#            print("Invalid CMR+ Subtype 3 length {}".format(Length))
#            return DCOL.Invalid_Decode

#        print("data: ", data)
#        print("data len: ", len(data))

        self.Short_Station=unpack_from('> 8s',data)[0]
        del data[0:calcsize('> 8s')]

        while len(self.Short_Station) > 0:
            if self.Short_Station[0] == 0 :
                self.Short_Station = self.Short_Station[1:]  # Delete for byte arrays
            else:
                break

        self.Short_Station=self.Short_Station.decode("CP850")

        self.COGO_Code=unpack_from('> 16s',data)[0]
        del data[0:calcsize('> 16s')]

        while len(self.COGO_Code) > 0:
            if self.COGO_Code[0] == 0 :
                self.COGO_Code = self.COGO_Code[1:]
            else:
                break

        self.COGO_Code = self.COGO_Code.decode("CP850")

#        print ("COGO:", self.COGO_Code)

        Station_Length=Length-26
        if Station_Length < 1 or Station_Length > 51:
            print("Invalid CMR+ 3 Subtype Station Length {}".format(Station_Length))
            return DCOL.Invalid_Decode


#        print ("Station Length: " ,Station_Length)
#        print (len(data))

        self.Long_Station=unpack_from('> {}s'.format(Station_Length),data)[0] #Remove the \00
        del data[0:calcsize('> {}s'.format(Station_Length))]
#        print (self.Long_Station)

        if self.Long_Station[len(self.Long_Station)-1] != 0:
            print("Invalid CMR+ 3 Subtype 3 End of Long Station not 0 {}".format(self.Long_Station[len(self.Long_Station)-1]))
            return DCOL.Invalid_Decode

        self.Long_Station=self.Long_Station[:-1]
        self.Long_Station = self.Long_Station.decode("CP850")
#        print (self.Long_Station)

        (self.stationName, self.code, self.basePointQuality, self.basePointType,self.errLocation, self.trackingDetails, self.antennaType, self.antennaMeasure, self.protocol) = decodeSCStation(self.Long_Station)

#        print (hexlify(self.Long_Station))
        return DCOL.Got_Packet




    def decode(self,data,internal=False):
        unpacked=unpack_from('> B B B',data)

        self.station_ID=unpacked[0]
        self.Page_Index=unpacked[1]
        self.Max_Page_Index=unpacked[2]
        self.pages_seen+=[self.Page_Index]
        self.packet_data_len=len(data)-3
        del data[0:3]
#        print(len(data))
#        pprint(data)
        self.packet_data.extend(data)
#        pprint(self.packet_data)
#        pprint(len(self.packet_data))

        result=DCOL.Got_Sub_Packet

        if self.Max_Page_Index == self.Page_Index: # Last Page
            if len (self.pages_seen) == self.Max_Page_Index+1 :
                result=DCOL.Got_Packet
                self.decode_Plus_buffer(self.packet_data)
            else:
                result=DCOL.Missing_Sub_Packet

            self.packet_data=bytearray(0)
            self.pages_seen=[]

        return result

    def dump(self,Dump_Level):

        if Dump_Level >= Dump_Summary :
            print(("Low Base Battery: {}, Low Base Memory: {}, L2 Enabled: {}".format(self.Low_Base_Battery,self.Low_Base_Memory,self.L2_Enabled)))
            print(("Motion: {}, Antenna Type: {}".format(TMotion_Names[self.Motion_State],self.Antenna_Type)))

        if Dump_Level >= Dump_Verbose :
            print(("Maxwell: {}, Reserved: {}".format(self.Maxwell,self.Reserved)))

        print(("   X (mm):            {:16.0f}  Y (mm): {:16.0f}  Z (mm): {:16.0f}".format(
            self.X,
            self.Y,
            self.Z)));

        print(("   Antenna Height (mm): {:6.0f}   East Offset (mm): {:6.0f} Northing Offset (mm): {:6.0f}".format(
            self.Antenna_Height,
            self.East_Offset,
            self.North_Offset)));

        print(("   Position Accuracy: {}".format(self.Position_Accuracy)))

        print(("   Short Station Name: {}".format(self.Short_Station)))
        print(("   Cogo code: {}".format(self.COGO_Code)))
        print(("   LongStation Name: {}".format(self.Long_Station)))
        if self.errLocation == None:
            print("      Encoded:")
            print("      Station Name: {}".format(self.stationName))
            print("      Code: {}".format(self.code))
            print("      Base Quality: {}".format(self.basePointQuality))
            print("      Base Type: {}".format(self.basePointType))
            print("      Tracking: {}".format(self.trackingDetails))
            print("      Antenna ID: {}".format(self.antennaType))
            print("      Antenna Measurement: {}".format(self.antennaMeasure))
            print("      Protocol: {}".format(self.protocol))
        else:
            print("      Not Encoded: {}".format(self.errLocation))



