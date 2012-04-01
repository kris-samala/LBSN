import sys
import fileinput
import pickle
import operator

#python remove_freq.py [location_data] freq.out fixed_freq.in removed.out

freq = []
users = []

out = open(sys.argv[3], 'wb')
removed = open(sys.argv[4], 'wb')

for l in fileinput.input(sys.argv[2]):
    line = l.split()
    freq.append(line[0])

for l in fileinput.input(sys.argv[1]):
    line = l.split('\t')
    user = line[7].rstrip()
    if user in freq:
        removed.write(l)
    else:
        out.write(l)

out.close()
removed.close()

