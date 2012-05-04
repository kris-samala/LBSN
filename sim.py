import sys
import random
import pickle
import math
import csv
import fileinput
from locations import LocationGraph
import numpy as np


#python simulation.py [n] [prob] contact_dist.out states.p census.p trans_prob.csv city_list.p matrix.out

#setup parameter values
time_steps = 180
n = int(sys.argv[1])
beta = float(sys.argv[2])
max_inf = 10
max_lat = 3

#load contact distribution
contacts = []
for line in fileinput.input(sys.argv[3]):
    line = line.rstrip(',').split(",")
    line = [int(x) for x in line]
    contacts.extend(line)

states = pickle.load(open(sys.argv[4], 'rb'))

#load census data
population = {}
census = pickle.load(open(sys.argv[5], 'rb'))
total_pop = 0
for p in census:
    total_pop += census[p]

for p in census:
    population[p] = (census[p] / float(total_pop)) * n

#load transition probability matrix
reader = csv.reader(open(sys.argv[6], 'rb'), delimiter=',')
T =[]
for row in reader:
    row = [(float(x) if x else 0) for x in row]
    T.append(np.array(row))

T = np.array(T)
city_list = pickle.load(open(sys.argv[7], 'rb'))

print "Dictionaries loaded."

#output file
params = str(beta)
matrix = open(sys.argv[8]+"_"+params+".out", 'w')

countID = 0
infected = {}
latent = {}
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
    a = .6
    omega = .017
    phi = 1.87
    lamda = .55
    return p * ((1-a)+a*math.pow(math.fabs(math.sin(omega*t+phi)),lamda))

def gen_latent(city, l):
    length = random.randint(1, max_lat)
    l[genID()] = (city, length)
    population[city] -= 1

    return l

def init_city(city, l):
    frac = .0001
    num = int(frac * population[city])
    print num
    for i in range(num):
        l.update(gen_latent(city, l))

    return l

def next_city(group, ID):
    curr_loc, t = group[ID]
    i = city_list.index(curr_loc)
    j = prob_index(T[i])
    curr_loc = city_list[j]
    return curr_loc

def infect_indiv(p):
    rand = random.random()
    return rand <= p

def infect_city(city, p, l):
    num = contacts[random.randint(0,len(contacts)-1)]
    new_infected = {}
    for i in range(num):
        if infect_indiv(p):
            l.update(gen_latent(city, l))

    return new_infected, l

def update_latent(i, l):
    remove = []
    for ID in l:
        curr_loc, t = l[ID]
        curr_loc = next_city(l,ID)
        t -= 1
        if t > 0:
            l[ID] = (curr_loc, t)
        else:
            remove.append(ID)

    for ID in remove:
        del l[ID]
        length = random.randint(1, max_inf)
        i[ID] = (curr_loc, length)

    return i, l

def spread(infected, l, t):
    new = {}
    remove = []
    sp = seasonal_prob(beta, t)
    for ID in infected:
        curr_loc, t = infected[ID]
        new_i, new_l = infect_city(curr_loc, sp, l)
        new.update(new_i)
        l.update(new_l)
        curr_loc = next_city(infected, ID)
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
    return infected, l


def stateStats(time_step):
    inf = {}
    si = [0]*50

    for id in infected:
        loc,t = infected[id]
        loc = loc.split(',')
        state = loc[1]
        if state in inf:
            inf[state] += 1
        else:
            inf[state] = 1

    for state in inf:
        index = states.index(state)
        si[index] = inf[state]

    return si

time_step = 0
infection_matrix = []

latent = init_city("New York,NY", latent)
while time_step < time_steps:
    infection_matrix.append(stateStats(time_step))

    time_step += 1
    if time_step == time_steps:
        break
    infected, latent = update_latent(infected, latent)
    infected, latent = spread(infected, latent, time_step)


for row in infection_matrix:
    matrix.write(str(row)+'\n')

matrix.close()

print "Simulation finished."
