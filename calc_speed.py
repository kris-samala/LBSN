import numpy as np
import sys
import pickle

#python calc_speed.py distance.p time_diff.p

distance = pickle.load(open(sys.argv[1], 'rb'))
time = pickle.load(open(sys.argv[2], 'rb'))

speed = []
sdist = []

for i in range(len(distance)):
    if time[i] > 0:
        speed.append(distance[i] / (time[i] * 24))
#        sdist.append(distance[i])

pickle.dump(speed, open('out/speed.p', 'wb'))
#pickle.dump(sdist, open('out/sdist.p', 'wb'))
