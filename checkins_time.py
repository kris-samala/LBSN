import sys
import fileinput
import pickle

#python checkins_time.py out/data_info.out

total = []
time = []

if len(sys.argv) < 2:
    print "Filename required."
else:
    for line in fileinput.input(sys.argv[1]):
        line = line.split()
        checkins = int(line[0])
        days = float(line[checkins])
        total.append(checkins)
        time.append(days)

pickle.dump(total, open('out/total_checkins.p', 'wb'))
pickle.dump(time, open('out/total_time.p', 'wb'))
