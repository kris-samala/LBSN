import sys
import fileinput
import pickle
import math
import operator
from datetime import datetime
from datetime import timedelta

#python fix_time.py fixed_locations.in timezones.in fixed_time.in

fmt = "%Y-%m-%d %H:%M:%S"
timezone = {}
out = open(sys.argv[3], 'wb')

for l in fileinput.input(sys.argv[2]):
    line = l.split()
    state = line[0]
    zone = line[1]
    if zone == "EST":
        timezone[state] = 0
    elif zone == "CST":
        timezone[state] = -1
    elif zone == "MST":
        timezone[state] = -2
    elif zone == "PST":
        timezone[state] = -3
    elif zone == "AKDT":
        timezone[state] = -4
    elif zone == "HST":
        timezone[state] = -6

for l in fileinput.input(sys.argv[1]):
    line = l.split('\t')
    state = line[3].lstrip()
    date = datetime.strptime(line[8].rstrip(), fmt)
    time_diff = timedelta(hours=timezone[state])
    date += time_diff
    datestring = date.strftime(fmt)
    pre = "\t".join(line[0:8])
    new_line = pre + '\t' + datestring + '\n'
    out.write(new_line)

out.close()
