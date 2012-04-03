import numpy as np
import matplotlib.pyplot as plt
import sys
import pickle


#python data_charts.py [xs] [ys] [xlabel] [ylabel] [min_val] [max_val] [output.png]
#max_val = 0 for no limit on values

xs = []
ys = []

min_val = float(sys.argv[5])
max_val = float(sys.argv[6])

raw_xs = pickle.load(open(sys.argv[1], 'rb'))
raw_ys = pickle.load(open(sys.argv[2], 'rb'))

if max_val > 0:
    for i in range(len(raw_xs)):
        if raw_xs > min_val and raw_xs[i] < max_val:
            xs.append(raw_xs[i])
            ys.append(raw_ys[i])
else:
    xs = raw_xs
    ys = raw_ys


fig = plt.figure()
ax = fig.add_subplot(111)

ax.set_xlabel(sys.argv[3])
ax.set_ylabel(sys.argv[4])

ax.scatter(xs, ys, s=5, alpha=.5)
#ax.hist(xs, alpha=.75)

plt.savefig(sys.argv[7]+"-"+str(min_val)+"-"+str(max_val)+".png")
