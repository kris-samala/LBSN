import sys
import random
import pickle
from locations import LocationGraph
#import matplotlib
#matplotlib.use('Agg')
import numpy as np
#import matplotlib.pyplot as plt

#python simulation.py [time_steps] [init_n] [n] [prob] out/locations.p citydata/census.p out/gowalla_net out/sim.out

time_steps = int(sys.argv[1])
init_n = int(sys.argv[2])
n = int(sys.argv[3])
prob = float(sys.argv[4])

locations=pickle.load(open(sys.argv[5], 'rb'))
#need to update with actual census data
population = {}
census = pickle.load(open(sys.argv[6], 'rb'))
total_pop = 0
for p in census:
    total_pop += census[p]

for p in census:
    population[p] = int ((census[p] / float(total_pop)) * n)

network = LocationGraph()
network.load(sys.argv[7])
print "Dictionaries loaded."

countID = 0
infected = {}
recovered = []

def genID():
    global countID
    countID += 1
    return countID

#choose location based on weight probabilities
def prob_index(probs):
    r, s = random.random(), 0

    for i in range(len(probs)):
        s += probs[i]
        if s >= r:
            return i

    print >> sys.stderr, "Error in prob_index"


#choose random location for each user
for i in range(init_n):
    city = random.choice(network.nodes())
    infected[genID()] = (city, 3)
    population[city] -= 1

def next_city(ID):
    curr_loc, t = infected[ID]
    sum_weight = float(network.total_edge_weights(curr_loc))
    poss_loc = network.neighbors(curr_loc)
    if len(poss_loc) > 0:
        probs = []  # edge or node weight divided by total weights
        for l in poss_loc:
            p = network.edge_weight(curr_loc, l) / sum_weight
            probs.append(p)
        poss_loc.append(curr_loc)

        #determine location to infect
        index = prob_index(probs)
        curr_loc = poss_loc[index]

    return curr_loc

def infect_indiv(p):
    rand = random.random()
    return rand <= p

def infect_city(city, p):
    gamma = np.random.gamma(1, 2.0) / 100
    pop = population[city]
    num = int(pop * gamma)
    new_infected = {}
    for i in range(num):
        if infect_indiv(p):
            new_infected[genID()] = (city, 3)
            population[city] -= 1
    return new_infected

def spread(infected):
    new = {}
    remove = []
    for ID in infected:
        curr_loc, t = infected[ID]
        new.update(infect_city(curr_loc, prob))
        curr_loc = next_city(ID)
        t -= 1
        if t > 0:
            infected[ID] = (curr_loc, t)
        else:
            remove.append(ID)
            recovered.append(ID)

    #update infected list
    for id in remove:
        del infected[id]
    infected.update(new)
    return infected


results = open(sys.argv[8], 'w')
time_step = 0

while time_step <= time_steps:
    print len(infected)
    results.write("Time step: " + str(time_step) + "\n")
    for id in infected:
        results.write(str(id) + str(infected[id]) + '\n')

    time_step += 1
    infected = spread(infected)

results.close()

#width = .5
#ind = [i for i in range(1, 10 + 1)]
#num_infected = [10, 36, 128, 514, 2608, 14091 , 80393, 469748, 2776384,
#        16550373]
#
#fig = plt.figure()
#ax = fig.add_subplot(111)
#
#rect = ax.bar(ind, num_infected, width, color='b')
#
#ax.set_xlabel("Time")
#ax.set_ylabel("# Infected")
#ax.set_title("Disease Simulation over Gowalla Network")
#ax.set_xticks([i+width for i in ind])
#ax.set_xticklabels(ind)
#
#plt.savefig("out/bargraph.png")
