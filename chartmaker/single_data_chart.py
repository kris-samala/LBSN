import numpy as np
import matplotlib.pyplot as plt
import sys
import pickle


#python data_charts.py [xs] [xlabel] [ylabel] [max_val] [output.png]
#max_val = 0 for no limit on values

xs = []

max_val = float(sys.argv[4])

raw_xs = pickle.load(open(sys.argv[1], 'rb'))

if max_val > 0:
    for i in range(len(raw_xs)):
        if raw_xs[i] < max_val:
            xs.append(raw_xs[i])
else:
    xs = raw_xs

fig = plt.figure()
ax = fig.add_subplot(111)

ax.set_xlabel(sys.argv[2])
ax.set_ylabel(sys.argv[3])

#ax.scatter(xs, ys, s=5, alpha=.5)
ax.hist(xs, alpha=.75)

plt.savefig(sys.argv[5]+"-"+str(max_val)+".png")
