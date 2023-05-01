
from ENUM import enum


def decodeSCStation (longStation):

    stationName=None
    code=None
    basePointQuality=None
    basePointType=None
    errLocation=None

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

    return( stationName, code, basePointQuality, basePointType,errLocation)
