import numpy as np
import matplotlib.pyplot as plt
import sys
import pickle


#python date_charts.py [year.p] [xlabel] [ylabel] [output.png]

xs = []
ys = []

dates = pickle.load(open(sys.argv[1], 'rb'))

print dates

for key, value in dates.iteritems():
    xs.append(key)
    ys.append(value)

fig = plt.figure()
ax = fig.add_subplot(111)

ax.set_xlabel(sys.argv[2])
ax.set_ylabel(sys.argv[3])

ax.plot(xs, ys, alpha=.5)
#ax.hist(xs, alpha=.75)

plt.savefig(sys.argv[4])
