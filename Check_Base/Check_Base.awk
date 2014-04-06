#!/usr/bin/env awk -f

BEGIN {
#    print ARGC
    if (ARGC == 2) {
        NAME=ARGV[1]
        ARGV[1]="-"
        print "Checking that the base name is: "  NAME >> "/dev/stderr"
    }
    else {
        print "Usage: Check_Base <Base Name>"
        print ""
        print "Checks the Received Base stream from DCOL_Decode.py, to make sure it has not changed"
        exit (1)
    }

}

/ Name: / {
    if (NAME != $4) {
        print "Base name is: " $4 " instead of " NAME
        system ("mail -s Base name is: " $4 " instead of " NAME " Geoffrey_Kirk@Trimble.com </dev/null")
    }
 }

END {
  print "Check Base Exited" >> "/dev/stderr"
}
