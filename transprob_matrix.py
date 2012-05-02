import sys
import fileinput
import pickle
import csv
from locations import LocationGraph
import numpy as np

#python transprob_matrix.py out/gowalla_net trans_prob.csv city_list.p

network = LocationGraph()
network.load(sys.argv[1])
city_list = network.nodes()
size = len(city_list)

T = np.zeros(shape=(size,size))

for i in range(size):
    city1 = city_list[i]
    sum_w = network.total_edge_weights(city1)
    for j in range(size):
        city2 = city_list[j]
        w = network.edge_weight(city1,city2)
        T[i,j] = w / float(sum_w)

writer = csv.writer(open(sys.argv[2], 'wb'), delimiter=',')

for row in T:
    writer.writerow(row)

pickle.dump(city_list, open(sys.argv[3], 'wb'))
