
from DCOL_Decls import *
from base64 import b64decode, standard_b64decode


def decodeSCStation (longStation):

    stationName=None
    code=None
    basePointQuality=None
    basePointType=None
    errLocation=None
    trackingDetails=None
    antennaType=None
    antennaMeasure=None
    protocol=None


    if longStation[0] != "@":
        errLocation=0
    elif longStation[1] != "A" and longStation[1] != " ":
        errLocation=1
    elif longStation[22] != "B" and longStation[22] != " ":
        errLocation=22
    elif longStation[39] != "D":
        errLocation=39
    elif longStation[40] != "A" and longStation[40] != "K" :
        errLocation=40
    elif longStation[41] != "N" and longStation[41] != "C" :
        errLocation=41
    elif longStation[len(longStation)-1] != "@":
        errLocation=-1

#    print(len(longStation))
#    print(longStation[42])

    if errLocation != None:
        return( stationName, code, basePointQuality, basePointType,errLocation)

    if longStation[1] == "A":
        stationName=longStation[2:18]

    if longStation[22] == "B":
        code=longStation[23:39]

    basePointQuality=longStation[40]
    basePointType=longStation[41]

    if len(longStation)==50:
        trackingDetails_char=longStation[42]
        trackingDetails=[]
        trackingDetails_byte=ord(trackingDetails_char)-ord('@')
        if (trackingDetails_byte & Bit0):
            trackingDetails+=["L2C"]
        if (trackingDetails_byte & Bit1):
            trackingDetails+=["L5"]
        if (trackingDetails_byte & Bit2):
            trackingDetails+=["GLONASS"]
        if (trackingDetails_byte & Bit3):
            trackingDetails+=["GLONASS-L1-P"]
        if (trackingDetails_byte & Bit4):
            trackingDetails+=["GLONASS-L2-C/A"]

        std_base64chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        antennaType_Hi=std_base64chars.index(longStation[43])
        antennaType_Lo=std_base64chars.index(longStation[44])
#        print ("Hi: {}, Lo: {}".format(antennaType_Hi,antennaType_Lo))
        antennaType=antennaType_Hi<<6 | antennaType_Lo

        antennaMeasure=longStation[45]
        protocol=longStation[46]



    return( stationName, code, basePointQuality, basePointType, errLocation, trackingDetails, antennaType, antennaMeasure, protocol)
