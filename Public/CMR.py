import DCOL

# Documentation Source: CMR Paper

from struct import *
from binascii import hexlify
from ENUM import enum
from DCOL_Decls import *
import numpy


class CMR (DCOL.Dcol) :
   def __init__ (self):

      self.version_number=None
      self.station_ID=None
      self.message_type=None
      self.Epoch_Time = None

      self.CMR=False
      self.MB=False
      self.CMRx=False
      self.Dummy=False

#Type 0 Header
      self.Clock_Bias_Valid = None
      self.Clock_Offset = None
      self.Number_SVs = None

#Type 1 _ 2 Header
      self.Low_Base_Battery=None
      self.Low_Base_Memory=None
      self.Maxwell=None
      self.L2_Enabled=None
      self.Reserved=None
      self.Motion_State = None
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
      self.stationName = None
      self.code = None
      self.basePointQuality = None
      self.basePointType  = None
      self.errLocation = None



   def decode_type_1_2_header(self,data):
      unpacked=unpack_from('> B',data)
      del data[0:calcsize('> B')]

      self.Low_Base_Battery=unpacked[0]& Bit4 != 0
      self.Low_Base_Memory=unpacked[0]& Bit3 != 0
      self.Maxwell=unpacked[0]& Bit2 != 0
      self.L2_Enabled=unpacked[0]& Bit1 != 0
      self.Reserved=unpacked[0]& Bit0 != 0

      unpacked=unpack_from('> H',data)
      del data[0:calcsize('> H')]
      self.Epoch_Time = unpacked[0] << 2

      unpacked=unpack_from('> B',data)
      del data[0:calcsize('> B')]
      self.Epoch_Time |= unpacked[0] >> 6 # High 2 bytes
      self.Motion_State = (unpacked[0] & (Bit5 | Bit4))>>4


      unpacked=unpack_from('> B',data)
      del data[0:calcsize('> B')]
      self.Antenna_Type=unpacked[0]
      return data


   def decode_type_1 (self,data):
      '''
      B := Buffer[CMR_Data_Offset + 7];
      I64 := B SHL (32-8);
      B := Buffer[CMR_Data_Offset + 8];
      I64 := I64 OR (B SHL (32-16));
      B := Buffer[CMR_Data_Offset + 9];
      I64 := I64 OR (B SHL (32-24 ));
      B := Buffer[CMR_Data_Offset + 10];
      I64 := I64 OR B;

      {Here we have a 32bit signed int, based on the 32 MS bits from the data}
      {Just move this over by 2 and add the new bits}

      B := Buffer[CMR_Data_Offset + 11];
      B := (B AND (BIT7 OR BIT6));
      B := B SHR 6;
      I64 := (I64 SHL 2);
      I64 := I64 OR B;
      IF (I64 AND $0000000200000000) <> 0 THEN
         BEGIN
         I64 := I64 OR ($FFFFFFFC00000000); {Sign extend}
         END;

      X := I64;

      W := Buffer[CMR_Data_Offset + 11];
      W := (W AND (NOT (BIT7 OR BIT6)));
      Antenna_Height := W SHL 8;

      W := Buffer[CMR_Data_Offset + 12];
      Antenna_Height := Antenna_Height OR W;
      '''


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
#      print self.Position_Accuracy

      return DCOL.Got_Packet

   def decode_type_2 (self,data):
      Length=numpy.uint8(unpack_from('> B',data)[0])
      del data[0:calcsize('> B')]
      self.Short_Station=unpack_from('> 8s',data)[0]
      del data[0:calcsize('> 8s')]
#      print self.Short_Station

      self.COGO_Code=unpack_from('> 16s',data)[0]
      del data[0:calcsize('> 16s')]
#      print self.COGO_Code

      Station_Length=Length-25 # The documentation is wrong on this. The range should be 26-75
#      print Station_Length
#      print len(data)
      self.Long_Station=unpack_from('> {}s'.format(Station_Length-1),data)[0] #Remove the \00
      del data[0:calcsize('> {}s'.format(Station_Length))]
#      print self.Long_Station
#      print hexlify(self.Long_Station)

      (self.stationName, self.code, self.basePointQuality, self.basePointType,self.errLocation) = decodeSCStation(self.Long_Station)



      return DCOL.Got_Packet


   def decode_type_0_header(self,data):

      unpacked=unpack_from('> B',data)
      del data[0:calcsize('> B')]
      self.Number_SVs=unpacked[0] & 0x1F

      unpacked=unpack_from('> H',data)
      del data[0:calcsize('> H')]
      self.Epoch_Time = unpacked[0] << 2
#      print unpacked[0],self.Epoch_Time

      unpacked=unpack_from('> B B',data)
      del data[0:calcsize('> B B')]
      self.Epoch_Time |= unpacked[0] >> 6 # High 2 bytes
      self.Clock_Bias_Valid = (unpacked[0] & (Bit5 | Bit4))>>4
      self.Clock_Offset  = (unpacked[0] & 0x0F )<<8
      self.Clock_Offset |= unpacked[1]
      return data




   def decode(self,data,internal=False):

      unpacked=unpack_from('> B B',data)
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

      if (self.message_type == 0):
         data=self.decode_type_0_header(data)
         return DCOL.Got_Packet
      elif (self.message_type == 1):
         self.Flags=unpacked[1] & 0x1F
         data=self.decode_type_1_2_header(data)
         return self.decode_type_1(data)
      elif (self.message_type == 2) :
         self.Flags=unpacked[1] & 0x1F
         data=self.decode_type_1_2_header(data)
         return self.decode_type_2(data)
      else :
         return DCOL.Got_Packet






   def dump(self,Dump_Level):

      if Dump_Level >= Dump_Summary :
#         print "Version Number: {:X}".format(self.version_number)
         if self.CMRx:
            print("CMRx")
            print(("   Type: {}  ID: {}".format(
               self.message_type,
               self.station_ID
               )))
         elif self.Dummy :
            print("Dummy CMR")
         else :
#            print "CMR Message: {}".format(self.message_type)
            if (self.message_type == 2) or (self.message_type==1) :
               if Dump_Level >= Dump_Summary :
                  print(("Epoch_Time: {}".format(self.Epoch_Time)))
                  print(("Low Base Battery: {}, Low Base Memory: {}, L2 Enabled: {}".format(self.Low_Base_Battery,self.Low_Base_Memory,self.L2_Enabled)))
                  print(("Motion: {}, Antenna Type: {}".format(TMotion_Names[self.Motion_State],self.Antenna_Type)))
               if Dump_Level >= Dump_Verbose :
                  print(("Maxwell: {}, Reserved: {}".format(self.Maxwell,self.Reserved)))

            if self.message_type == 1:
               print(("   X (mm):            {:16.0f}  Y (mm): {:16.0f}  Z (mm): {:16.0f}".format(
               self.X,
               self.Y,
               self.Z)));
               print(("   Antenna Height (mm): {:6.0f}   East Offset (mm): {:6.0f} Northing Offset (mm): {:6.0f}".format(
               self.Antenna_Height,
               self.East_Offset,
               self.North_Offset)));
               print(("   Position Accuracy: {}".format(self.Position_Accuracy)))

            elif self.message_type == 2:
               print(("   Short Station Name: {}".format(self.Short_Station)))
               print(("   Cogo code: {}".format(self.COGO_Code)))
               print(("   LongStation Name: {}".format(self.Long_Station)))
               if self.errLocation == None:
                  print("      Encoded:")
                  print("      Station Name: {}".format(self.stationName))
                  print("      Code: {}".format(self.code))
                  print("      Base Quality: {}".format(self.basePointQuality))
                  print("      Base Type: {}".format(self.basePointType))
               else:
                  print("      Not Encoded: {}".format(self.errLocation))

            else :
               print(("   Type: {}  ID: {}  Version: {}".format(
               self.message_type,
               self.station_ID,
               self.version_number)));

