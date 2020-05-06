#!/usr/bin/env python3
#from __future__ import division
import sys
import argparse
import pprint
import time
import datetime
import socket


sys.path.append("Public"); # Gave up trying to work how to do this with a .pth file or using .
sys.path.append("/Users/gkirk/Documents/GitHub/DCOL")
sys.path.append("/Users/gkirk/Documents/GitHub/DCOL/Public")
sys.path.append("/Users/gkirk/Dropbox/Develop/python/DCOL/internal")
sys.path.append("internal");
sys.path.append("internal_stubs");

from DCOL import *
from DCOL_Decls import *
import sys
from datetime import datetime

try:
   from JCMBSoftPyLib import GPS_TIME
except:
   print ("JCMBSoftPyLib is not installed. Download and install from https://github.com/jcmb/JCMBSoftPyLib.git")

GPS_Offset=18

def ByteToHex( byteStr ):
    """
    Convert a byte string to it's hex string representation e.g. for output.
    """

    hex = []
    for aChar in byteStr:
        hex.append( "%02X " % aChar )

    return ''.join( hex ).strip()


class ArgParser(argparse.ArgumentParser):

    def convert_arg_line_to_args(self, arg_line):
        for arg in arg_line.split():
            if not arg.strip():
                continue
            yield arg


parser = ArgParser(
            description='Trimble CMR Timer',
            fromfile_prefix_chars='@',
            epilog="(c) JCMBsoft 2013-2020")

parser.add_argument("-P", "--CMRPlus", action="store_true", help="Displays Time For CMR+ Packets Only")
parser.add_argument("-C", "--CMR", action="store_true", help="Displays Time For CMR Packets Only (Really CMR at the moment)")
parser.add_argument("-X", "--CMRx", action="store_true", help="Display Time for CMRx Packets Only")
parser.add_argument("-M", "--MB", action="store_true", help="Display Time for MB CMR Packets Only (Really CMR at the moment)")
parser.add_argument("-I", "--IP", nargs=2, help="Server Port. Connect via TCP To a device instead of reading from StdIn,")
parser.add_argument("-O", "--Output",help="Output file, instead of writing to StdOut")

args=parser.parse_args()


dcol=Dcol(internal=False,default_output_level=0);

Time_CMRPlus=True
Time_CMR=True
Time_CMRx=True
Time_CMRG=True
Time_MB=False

if args.CMRPlus:
   sys.stdout.write("CMRPlus:\n");
   Time_CMRPlus=True
   Time_CMR=False
   Time_CMRx=False
   Time_MB=False
   Time_CMRG=False

if args.CMR:
   sys.stdout.write("CMR:\n");
   Time_CMRPlus=False
   Time_CMR=True
   Time_CMRx=False
   Time_MB=False
   Time_CMRG=False

if args.CMRx:
   sys.stdout.write("CMRx:\n");
   Time_CMRPlus=False
   Time_CMR=False
   Time_CMRx=True
   Time_MB=False
   Time_CMRG=False

if args.MB:
   sys.stdout.write("CMR Moving Base:\n");
   Time_CMRPlus=False
   Time_CMR=False
   Time_CMRx=False
   Time_MB=True
   Time_CMRG=False


last_time=None
#with open ('DCOL.bin','rb') as input_file:
#   new_data = bytearray(input_file.read(255))

if args.IP == None:
    sys.stderr.write("Using Standard Input\n")
    Use_TCP=False
    new_data = bytearray(sys.stdin.read(1))
else:
    sys.stderr.write("Using TCP\n")
    Use_TCP=True
    HOST = args.IP[0]
    PORT = int(args.IP[1])
    Remote_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Remote_TCP.connect((HOST, PORT))
    new_data = Remote_TCP.recv(1)

if args.Output:
   output_file=open(args.Output,"a")
else:
   output_file=sys.stdout

output_file.write("Test Started\n")
last_ts = time.time()+GPS_Offset

while (new_data):

   dcol.add_data (data=new_data)
   result = dcol.process_data (dump_decoded=False)

   while result != 0 :
#        print str(datetime.now())
#      print (result)
      if result == Got_Packet :
#         print ("Got_Packet {} {}\n".format(dcol.packet_ID,CMR_Type_TrimComm_Command))
         now=datetime.utcnow()

         if (Time_CMRG or Time_MB) and dcol.packet_ID == CMRW_TrimComm_Command:
            if last_time:
               output_file.write("CMRG,{:X},{},{},{},{}\n".format(dcol.packet_ID,0,dcol.Packet_Data_Length+6,(now-last_time).total_seconds(),now))
            last_time = now

         if Time_CMRPlus and dcol.packet_ID == CMR_PLUS_TrimComm_Command:
            if last_time:
               output_file.write("CMR+,{:X},{},{},{},{}\n".format(dcol.packet_ID,5,dcol.Packet_Data_Length+6,(now-last_time).total_seconds(),now))
            last_time = now

         if (Time_CMR or Time_CMRPlus) and dcol.packet_ID == CMR_Type_TrimComm_Command:
#            print ("In CMR")
            if dcol.Handlers[CMR_Type_TrimComm_Command].CMR:
               ts = time.time()+GPS_Offset
               Week=GPS_TIME.DateTime_To_Week (ts)
               Secs=int(GPS_TIME.DateTime_To_Seconds_Of_Week (ts))
               Secs_Mod=Secs-(Secs % 240)

#               print (dcol.Handlers[CMR_Type_TrimComm_Command].station_ID)
#               print (dcol.Handlers[CMR_Type_TrimComm_Command].Epoch_Time)
               packet_time=GPS_TIME.Week_Seconds_To_Time (Week,Secs_Mod+dcol.Handlers[CMR_Type_TrimComm_Command].Epoch_Time/1000)
               delay_last_packet=last_ts-packet_time
               delay=ts-packet_time
#               print delay, delay_last_packet

#               print (dcol.Handlers[CMR_Type_TrimComm_Command].Number_SVs)
               if last_time:
                  output_file.write("CMR,{:X},{},{},{:.04f},{:.04f},{}\n".format(dcol.packet_ID,dcol.Handlers[CMR_Type_TrimComm_Command].message_type,dcol.Packet_Data_Length+6,(now-last_time).total_seconds(),delay,now))
               last_time = now
               last_ts = ts

         if Time_CMRx and dcol.packet_ID == CMR_Type_TrimComm_Command:
            if dcol.Handlers[CMR_Type_TrimComm_Command].CMRx:
               if last_time:
                  output_file.write("CMRx,{:X},{},{},{},{}\n".format(dcol.packet_ID,dcol.Handlers[CMR_Type_TrimComm_Command].message_type,dcol.Packet_Data_Length+6,(now-last_time).total_seconds(),now))
               last_time = now


         if Time_MB and dcol.packet_ID == CMR_Type_TrimComm_Command:
#            dcol.Handlers[CMR_Type_TrimComm_Command].dump(4)
            if (dcol.Handlers[CMR_Type_TrimComm_Command].MB) or (dcol.Handlers[CMR_Type_TrimComm_Command].CMR):
               if last_time:
                  output_file.write("MB,{:X},{},{},{},{}\n".format(dcol.packet_ID,dcol.Handlers[CMR_Type_TrimComm_Command].message_type,dcol.Packet_Data_Length+6,(now-last_time).total_seconds(),now))
               last_time = now
               last_ts = ts


         output_file.flush()
      result = dcol.process_data ()
#      print "processed: " + str(result)

   if Use_TCP:
       new_data = bytearray(Remote_TCP.recv(1))
   else:
       new_data = bytearray(sys.stdin.read(1))

if Use_TCP:
    Remote_TCP.close()

sys.stderr.write("Bye")

