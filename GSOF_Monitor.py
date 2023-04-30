#!/usr/bin/env python

import sys
import argparse
import pprint
from datetime import datetime
import socket


sys.path.append("Public"); # Gave up trying to work how to do this with a .pth file or using .
sys.path.append("internal");
sys.path.append("internal_stubs");

from DCOL import *
from DCOL_Decls import *
from GSOF import GNSS_System_Names


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



def process_arguments():
    parser = ArgParser(
                description='Trimble GSOF Montior',
                fromfile_prefix_chars='@',
                epilog="(c) Trimble 2021")

    parser.add_argument("-U", "--Undecoded", action="store_true", help="Displays Undecoded Packets")
    parser.add_argument("-D", "--Decoded", action="store_true", help="Displays Decoded Packets")
    parser.add_argument('-v', '--Verbose', action='count', default=0)
    parser.add_argument("-E", "--Explain", action="store_true", help="System Should Explain what is is doing, AKA Verbose")
    parser.add_argument("-W", "--Time", action="store_true", help="Report the time when the packet was received")
    parser.add_argument("-P", "--Primary", required=True, nargs=2, help="Server Port. Connect via TCP To the primary device.")
    parser.add_argument("-S", "--Secondary", required=True, nargs=2, help="Server Port. Connect via TCP To the secondary device.")

    args=parser.parse_args()

    if args.Explain:
        print(("Dump undecoded: {},  Dump Decoded: {} Time: {}, Verbose: {}".format(
            args.Undecoded,
            args.Decoded,
            args.Time,
            args.Verbose)))

    return(args)


def setup_nework(args):

    Use_TCP=True
    primaryHost = args.Primary[0]
    primaryPort = int(args.Primary[1])

    secondaryHost = args.Secondary[0]
    secondaryPort = int(args.Secondary[1])

    primaryTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    secondaryTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    primaryTCP.connect((primaryHost, primaryPort))
    secondaryTCP.connect((secondaryHost, secondaryPort))

    return(primaryTCP,secondaryTCP)


def get_GSOF(dcol,tcp,args):

    raw_data = tcp.recv(1)

    while (raw_data):
        dcol.add_data (data=raw_data)

        result = dcol.process_data (dump_decoded=args.Decoded)

#        print("While result " + str(result) )
        while result != 0 :
            if result == Got_Undecoded :
                if args.Undecoded :
                    print(("Undecoded Primary Data: " +ByteToHex(dcol.undecoded)));
            elif result == Got_Packet :
                if args.Verbose:
                    dcol.dump(dump_undecoded=args.Undecoded,dump_decoded=args.Decoded,dump_timestamp=args.Time);
                    sys.stdout.flush()
                return(dcol.Handlers[GENOUT_TrimComm_Command])
            elif result == Got_Sub_Packet:
                if args.Verbose>2:
                    print((dcol.name() + ' ( ' +  hex(dcol.packet_ID) +" ) : "))
                    print(" Sub packet of mutiple packet message")
                    print("")
                    sys.stdout.flush()
            elif result == Missing_Sub_Packet:
                if args.Verbose :
                    print((dcol.name() + ' ( ' +  hex(dcol.packet_ID) +" ) : "))
                    print(" Final sub packet of mutiple packet message, missed a sub packet.")
                    print("")
                    sys.stdout.flush()
            else :
                    print("INTERNAL ERROR: Unknown result")
                    sys.exit();
    #        print "processing"

            result = dcol.process_data (dump_decoded=args.Decoded)
    #        print "processed: " + str(result)
        raw_data = tcp.recv(1)


def process_GSOFs(primary,secondary):
    GPS=0
    SBAS=1
    GLONASS=2
    GALILEO=3
    QZSS=4
    BDS=5
    MSS=10

    primary_SVs={}
    primary_SVs[GPS]={}
    primary_SVs[SBAS]={}
    primary_SVs[GLONASS]={}
    primary_SVs[GALILEO]={}
    primary_SVs[QZSS]={}
    primary_SVs[BDS]={}
    primary_SVs[MSS]={}

    for SV in range(0,primary.Detailed_All_Num_SVs):
#        pprint(SV)
#        pprint(primary.SV_Detailed_All[SV])
#        pprint(primary.SV_Detailed_All[SV][8])
        primary_SVs[primary.SV_Detailed_All[SV][1]][primary.SV_Detailed_All[SV][0]]=(
            [
            primary.SV_Detailed_All[SV][6]/4.0,
            primary.SV_Detailed_All[SV][7]/4.0,
            primary.SV_Detailed_All[SV][8]/4.0
            ])

#    pprint(primary_SVs)

    for SV in range(0,secondary.Detailed_All_Num_SVs):
#        pprint(SV)
#        pprint(secondary.SV_Detailed_All[SV])
#        pprint(primary.SV_Detailed_All[SV][8])
        SV_System=secondary.SV_Detailed_All[SV][1]
        SV_Number=secondary.SV_Detailed_All[SV][0]
#        print(SV_System,SV_Number)
        if SV_Number in primary_SVs[SV_System]:
#            print(primary_SVs[SV_System][SV_Number])
#            pprint(secondary.SV_Detailed_All[SV])
            L1_Delta = primary_SVs[SV_System][SV_Number][0]-secondary.SV_Detailed_All[SV][6]/4.0
            L2_Delta = primary_SVs[SV_System][SV_Number][1]-secondary.SV_Detailed_All[SV][7]/4.0
            L5_Delta = primary_SVs[SV_System][SV_Number][2]-secondary.SV_Detailed_All[SV][8]/4.0
            print(("{},{},{},{},{},{}".format(primary.GPS_Time, GNSS_System_Names[SV_System], SV_Number, L1_Delta,L2_Delta,L5_Delta)))
#            print (primary.GPS_Time, GNSS_System_Names[SV_System], SV_Number, L1_Delta,L2_Delta,L5_Delta)
        else:
            print(("{},{},{},{},{},{}".format(primary.GPS_Time, GNSS_System_Names[SV_System], SV_Number, -99,-99,-99)))




def main():

    args=process_arguments()
    (primaryTCP,secondaryTCP)=setup_nework(args)

    primaryDcol=Dcol(internal=False,default_output_level=(3 if args.Verbose else 0));
    secondaryDcol=Dcol(internal=False,default_output_level=(3 if args.Verbose else 0));

    primaryGSOF=get_GSOF(primaryDcol,primaryTCP,args)
    if (primaryGSOF.seen_subrecords ^ {1, 2, 15, 48}):
        pprint(primaryGSOF.seen_subrecords)
        sys.exit("Error: Primary GSOF Outputs incorrect. Should be 1,15,48");

    secondaryGSOF=None
    secondaryGSOF=get_GSOF(secondaryDcol,secondaryTCP,args)
    if (secondaryGSOF.seen_subrecords ^ {1, 2, 15, 48}):
        pprint(secondaryGSOF.seen_subrecords)
        sys.exit("Error: Secondary GSOF Outputs incorrect. Should be 1,15,48");

    if primaryGSOF.Serial_Number == secondaryGSOF.Serial_Number:
        sys.exit("Error:Both units are the same!");

    # Here we have a GSOF from both units. We need to get them in sync.


    #TODO: Note that this will not work over a week rollover

    while primaryGSOF.GPS_Time < secondaryGSOF.GPS_Time:
        primaryGSOF=get_GSOF(primaryDcol,primaryTCP,args)

    while primaryGSOF.GPS_Time > secondaryGSOF.GPS_Time:
        secondaryGSOF=get_GSOF(secondaryDcol,secondaryTCP,args)

    # Here we have two GSOF messages at the same time tag.

    while True: #This assumes that they are both at the same rate since we don't resync
        process_GSOFs(primaryGSOF,secondaryGSOF)
        primaryGSOF=get_GSOF(primaryDcol,primaryTCP,args)
        secondaryGSOF=get_GSOF(secondaryDcol,secondaryTCP,args)



    primaryTCP.close()
    secondaryTCP.close()

    print("Bye")

if __name__ == '__main__':
    main()


