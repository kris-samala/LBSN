import sys
import fileinput
import pickle

#python distance_time.py out/data_info.out

distance = []
time_diff = []

if len(sys.argv) < 2:
    print "Filename required."
else:
    for line in fileinput.input(sys.argv[1]):
        line = line.split()
        total = int(line[0])
        line.pop(0)
        line.pop(total-1)
        for pair in line:
            pair = pair.split(',')
            distance.append(float(pair[0]))
            time_diff.append(float(pair[1]))

pickle.dump(distance, open('out/distance.p', 'wb'))
pickle.dump(time_diff, open('out/time_diff.p', 'wb'))
