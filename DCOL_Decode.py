#!/usr/bin/env python

import sys
import argparse
import pprint
from datetime import datetime
import socket


sys.path.append("Public"); # Gave up trying to work how to do this with a .pth file or using .
sys.path.append("/Users/gkirk/Dropbox/Develop/Python/DCOL/Internal")
sys.path.append("/Users/gkirk/Documents/GitHub/DCOL")
sys.path.append("/Users/gkirk/Documents/GitHub/DCOL/Public")
sys.path.append("internal");
sys.path.append("internal_stubs");

from DCOL import *
from DCOL_Decls import *


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
            description='Trimble Data Collector (DCOL) packet decoder',
            fromfile_prefix_chars='@',
            epilog="(c) JCMBsoft 2013-2014")

parser.add_argument("-A", "--ACK", action="store_true", help="Displays ACK/NACK replies")
parser.add_argument("-U", "--Undecoded", action="store_true", help="Displays Undecoded Packets")
parser.add_argument("-D", "--Decoded", action="store_true", help="Displays Decoded Packets")
parser.add_argument("-T", "--Trimble", action="store_true", help="Use internal decoders, which must be available.")
parser.add_argument("-L", "--Level", type=int, help="Output level, how much detail will be displayed. Default=2", default=2, choices=[0,1,2,3,4])
parser.add_argument("-N", "--None", nargs='+', help="Packets that should not be dumped")
parser.add_argument("-I", "--ID", nargs='+', help="Packets that should have there ID dumped only")
parser.add_argument("-S", "--Summary", nargs='+', help="Packets that should have a Summary dumped")
parser.add_argument("-F", "--Full", nargs='+', help="Packets that should be dumped Fully")
parser.add_argument("-V", "--Verbose", nargs='+', help="Packets that should be dumped Verbosely")
parser.add_argument("-E", "--Explain", action="store_true", help="System Should Explain what is is doing, AKA Verbose")
parser.add_argument("-G", "--GNSS", action="store_true", help="Data is from a GNSS Debug Traffic Stream. There are two bytes in front of each Packet")
parser.add_argument("-W", "--Time", action="store_true", help="Report the time when the packet was received")
parser.add_argument("-P", "--IP", nargs=2, help="Server Port. Connect via TCP To a device instead of reading from StdIn,")
parser.add_argument("-R", "--Raw", nargs=1, help="File to Log Raw Data to")

args=parser.parse_args()

#print args

Dump_Undecoded = args.Undecoded
Dump_Decoded = args.Decoded
Dump_TimeStamp = args.Time
Print_ACK_NAK  = args.ACK

if args.Explain:
    print "Dump undecoded: {},  Dump Decoded: {},  Dump ACK/NACK: {}, Dump TimeStamp: {}".format(
        Dump_Undecoded,
        Dump_Decoded,
        Print_ACK_NAK,
        Dump_TimeStamp)



dcol=Dcol(internal=args.Trimble,default_output_level=args.Level);

if args.Explain:
     print "Default Output Level: "  + str(args.Level)

if args.None:
    for id in args.None:
        if args.Explain:
            print "Decode Level None: " + hex(int(id,0))
        dcol.Dump_Levels[int(id,0)]=Dump_None

if args.ID:
    for id in args.ID:
        if args.Explain:
            print "Decode Level ID: " + hex(int(id,0))
        dcol.Dump_Levels[int(id,0)]=Dump_ID

if args.Summary:
    for id in args.Summary:
        if args.Explain:
            print "Decode Level Summary: " + hex(int(id,0))
        dcol.Dump_Levels[int(id,0)]=Dump_Summary

if args.Full:
    for id in args.Full:
        if args.Explain:
            print "Decode Level Full: " + hex(int(id,0))
        dcol.Dump_Levels[int(id,0)]=Dump_Full

if args.Verbose:
    for id in args.Verbose:
        if args.Explain:
            print "Decode Level Verbose: " + hex(int(id,0))
        dcol.Dump_Levels[int(id,0)]=Dump_Verbose

if args.GNSS:
   dcol.Set_Traffic(True)
   if args.Explain:
      print "Traffic Mode"



#with open ('DCOL.bin','rb') as input_file:
#   new_data = bytearray(input_file.read(255))


#print args.IP
if args.IP == None:
    print "Using Standard Input"
    Use_TCP=False
    new_data = bytearray(sys.stdin.read(1))
else:
    print "Using TCP"
    Use_TCP=True
    HOST = args.IP[0]
    PORT = int(args.IP[1])
    Remote_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Remote_TCP.connect((HOST, PORT))
    new_data = Remote_TCP.recv(1)

Log_Raw=False

if args.Raw:
    Log_Raw=True
    Raw_File=open(args.Raw[0]+".BIN","wb")

while (new_data):
    if Log_Raw:
        Raw_File.write(new_data)
    dcol.add_data (data=new_data)
#    new_data = input_file.read(255)
#    if len(dcol.buffer):
#        print str(len(dcol.buffer)) + ' ' + hex(dcol.buffer[len(dcol.buffer)-1])
#        sys.stdout.flush()
    result = dcol.process_data (dump_decoded=False)

    while result != 0 :
#        print str(datetime.now())
        if result == Got_ACK :
            if Print_ACK_NAK:
                print "ACK"
                print ""
        elif result == Got_NACK :
            if Print_ACK_NAK:
                print "NACK"
                print ""
        elif result == Got_Undecoded :
            if Dump_Undecoded :
                print "Undecoded Data: " +ByteToHex(dcol.undecoded);
        elif result == Got_Packet :
            dcol.dump(dump_undecoded=Dump_Undecoded,dump_decoded=Dump_Decoded,dump_timestamp=Dump_TimeStamp);
            sys.stdout.flush()
        elif result == Got_Sub_Packet:
            if dcol.Dump_Levels[dcol.packet_ID] :
                print dcol.name() + ' ( ' +  hex(dcol.packet_ID) +" ) : "
                print " Sub packet of mutiple packet message"
                print ""
                sys.stdout.flush()
        elif result == Missing_Sub_Packet:
            if dcol.Dump_Levels[dcol.packet_ID] :
                print dcol.name() + ' ( ' +  hex(dcol.packet_ID) +" ) : "
                print " Final sub packet of mutiple packet message, missed a sub packet."
                print ""
                sys.stdout.flush()
        else :
                print "INTERNAL ERROR: Unknown result"
                sys.exit();
#        print "processing"
        result = dcol.process_data ()
#        print "processed: " + str(result)
    if Use_TCP:
        new_data = Remote_TCP.recv(1)
    else:
        new_data = sys.stdin.read(1)

if Use_TCP:
    Remote_TCP.close()

if Log_Raw:
    Raw_File.close()
print "Bye"

