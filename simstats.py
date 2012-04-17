import pickle
import sys
import fileinput
import numpy as np

#python simstats.py [maps] > simstats.out

incidences = []

for l in fileinput.input(sys.argv[1]):
    line = l.split(",")
    for pair in line:
        if len(pair) > 1:
            p = pair.split(":")
            incidences.append(int(p[1]))

print "Min = " + str(np.min(incidences))
print "Max = " + str(np.max(incidences))
print "Mean = " + str(np.mean(incidences))
print "Median = " + str(np.median(incidences))
print "Std = " + str(np.std(incidences))
