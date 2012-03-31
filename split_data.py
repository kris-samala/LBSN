#!/usr/bin/env python

#python split_data.py [gowalla_raw] [output]
#extract the following fields from original raw data
#spotID, spotname, city, state, longitude, latitude, checkinID, userID, time

import sys
import fileinput

loc_string = ""

location_data = open(sys.argv[2], 'wb')

if len(sys.argv) < 2:
    print "Filename required."
else:
    #read input file
    for line in fileinput.input(sys.argv[1]):
        if not fileinput.isfirstline():
            line = line.split("\t")
            if (len(line) == 28):
                loc_string = line[1] + "\t" + line[5] + "\t" + line[6] + "\t " + line[7] + "\t" + line[12] + "\t" + line[13] + "\t" + line[21] + "\t" + line[23] + "\t" + line[25] +"\n"
                location_data.write(loc_string)

location_data.close()
