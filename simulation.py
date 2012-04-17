import sys
import random
import pickle
import math
from locations import LocationGraph
#import matplotlib
#matplotlib.use('Agg')
import numpy as np
#import matplotlib.pyplot as plt

#python simulation.py [time_steps] [init_n] [n] [prob] [gamma] [sine] locations.p census.p gowalla_net sim.out map.out

time_steps = int(sys.argv[1])
init_n = int(sys.argv[2])
n = int(sys.argv[3]) # not being used currently
prob = float(sys.argv[4])
theta = float(sys.argv[5])
omega = float(sys.argv[6])

locations=pickle.load(open(sys.argv[7], 'rb'))
#need to update with actual census data
population = {}
census = pickle.load(open(sys.argv[8], 'rb'))
total_pop = 0
for p in census:
    total_pop += census[p]

for p in census:
    population[p] = (census[p] / float(total_pop)) * n

#print population

network = LocationGraph()
network.load(sys.argv[9])
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

def seasonal_prob(p, t):
    return p * math.sin(omega*t)


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
        poss_loc.append(curr_loc)
        for l in poss_loc:
            p = network.edge_weight(curr_loc, l) / sum_weight
            probs.append(p)

        #determine location to infect
        index = prob_index(probs)
        curr_loc = poss_loc[index]

    return curr_loc

def infect_indiv(p):
    rand = random.random()
    return rand <= p

def infect_city(city, p):
    gamma = np.random.gamma(1, theta) / 100.0
    pop = population[city]
    num = int(pop * gamma)
    new_infected = {}
    for i in range(num):
        if infect_indiv(p):
            new_infected[genID()] = (city, 3)
            population[city] -= 1

    return new_infected

def spread(infected, t):
    new = {}
    remove = []
    sp = seasonal_prob(prob, t)
    for ID in infected:
        curr_loc, t = infected[ID]
        new.update(infect_city(curr_loc, sp))
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


def stateStats(time_step, out):
    inf = {}

    for id in infected:
        loc,t = infected[id]
        loc = loc.split(',')
        state = loc[1]
        if state in inf:
            inf[state] += 1
        else:
            inf[state] = 1

    for state in inf:
        out.write(state + ":" + str(inf[state]) + ",")
    out.write("\n")



params = str(prob) + "-" + str(theta) + "-" + str(omega)

results = open(sys.argv[10]+"_"+params+".out", 'w')
results.write("Simulation Parameters: " + str(init_n) + "-" + str(n) + "-" + params + "\n")

maps = open(sys.argv[11]+"_"+params+".out", 'w')

time_step = 0

while time_step <= time_steps:
    print len(infected)
    results.write("Time step: " + str(time_step) + " -> "+str(len(infected)) + "\n")
    for id in infected:
        results.write(str(id) + str(infected[id]) + '\n')

    time_step += 1
    infected = spread(infected, time_step)
    stateStats(time_step, maps)

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
