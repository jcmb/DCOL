#!/usr/bin/env python

import sys
import argparse
import pprint


sys.path.append("Public"); # Gave up trying to work how to do this with a .pth file or using .
sys.path.append("/Users/gkirk/Dropbox/git/DCOL/")
sys.path.append("/Users/gkirk/Dropbox/git/DCOL/Public")
sys.path.append("/Users/gkirk/Dropbox/Develop/python/DCOL/internal")
sys.path.append("internal");
sys.path.append("internal_stubs");

from DCOL import *
from DCOL_Decls import *
import sys
from datetime import datetime


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
            epilog="(c) JCMBsoft 2013")

parser.add_argument("-P", "--CMRPlus", action="store_true", help="Displays Time For CMR+ Packets Only")
parser.add_argument("-C", "--CMR", action="store_true", help="Displays Time For CMR Packets Only (Really CMR at the moment)")
parser.add_argument("-X", "--CMRx", action="store_true", help="Display Time for CMRx Packets Only")
parser.add_argument("-M", "--MB", action="store_true", help="Display Time for MB CMR Packets Only (Really CMR at the moment)")

args=parser.parse_args()


dcol=Dcol(internal=False,default_output_level=0);

Time_CMRPlus=True
Time_CMR=True
Time_CMRx=True
Time_MB=True

if args.CMRPlus:
   sys.stdout.write("CMRPlus:\n");
   Time_CMRPlus=True
   Time_CMR=False
   Time_CMRx=False
   Time_MB=False

if args.CMR:
   sys.stdout.write("CMR:\n");
   Time_CMRPlus=False
   Time_CMR=True
   Time_CMRx=False
   Time_MB=False

if args.CMRx:
   sys.stdout.write("CMRx:\n");
   Time_CMRPlus=False
   Time_CMR=False
   Time_CMRx=True
   Time_MB=False

if args.MB:
   sys.stdout.write("CMR Moving Base:\n");
   Time_CMRPlus=False
   Time_CMR=False
   Time_CMRx=False
   Time_MB=True


last_time=None
#with open ('DCOL.bin','rb') as input_file:
#   new_data = bytearray(input_file.read(255))
new_data = bytearray(sys.stdin.read(1))
while (new_data):

   dcol.add_data (data=new_data)
   result = dcol.process_data (dump_decoded=False)

   while result != 0 :
#        print str(datetime.now())
#      print result
      if result == Got_Packet :
         now=datetime.utcnow()
#         print "Got Packet: {:X}".format(dcol.packet_ID)

         if (Time_CMR or Time_MB) and dcol.packet_ID == CMRW_TrimComm_Command:
            if last_time:
               print "CMRG,{:X},{},{},{},{}".format(dcol.packet_ID,0,dcol.Packet_Data_Length+6,(now-last_time).total_seconds(),now)
            last_time = now

         if Time_CMRPlus and dcol.packet_ID == CMR_PLUS_TrimComm_Command:
            if last_time:
               print "CMR+,{:X},{},{},{},{}".format(dcol.packet_ID,5,dcol.Packet_Data_Length+6,(now-last_time).total_seconds(),now)
            last_time = now

         if (Time_CMR or Time_CMRPlus) and dcol.packet_ID == CMR_Type_TrimComm_Command:
            if dcol.Handlers[CMR_Type_TrimComm_Command].CMR:
               if last_time:
                  print "CMR,{:X},{},{},{},{}".format(dcol.packet_ID,dcol.Handlers[CMR_Type_TrimComm_Command].message_type,dcol.Packet_Data_Length+6,(now-last_time).total_seconds(),now)
               last_time = now

         if Time_CMRx and dcol.packet_ID == CMR_Type_TrimComm_Command:
            if dcol.Handlers[CMR_Type_TrimComm_Command].CMRx:
               if last_time:
                  print "CMRx,{:X},{},{},{},{}".format(dcol.packet_ID,dcol.Handlers[CMR_Type_TrimComm_Command].message_type,dcol.Packet_Data_Length+6,(now-last_time).total_seconds(),now)
               last_time = now

         if Time_MB and dcol.packet_ID == CMR_Type_TrimComm_Command:
#            dcol.Handlers[CMR_Type_TrimComm_Command].dump(4)
            if (dcol.Handlers[CMR_Type_TrimComm_Command].MB) or (dcol.Handlers[CMR_Type_TrimComm_Command].CMR):
               if last_time:
                  print "MB,{:X},{},{},{},{}".format(dcol.packet_ID,dcol.Handlers[CMR_Type_TrimComm_Command].message_type,dcol.Packet_Data_Length+6,(now-last_time).total_seconds(),now)
               last_time = now

         sys.stdout.flush()
      result = dcol.process_data ()
#      print "processed: " + str(result)
   new_data = sys.stdin.read(1)

print "Bye"

