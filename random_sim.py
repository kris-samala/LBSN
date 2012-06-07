from util2 import Util
import numpy as np
import fileinput
import random
import pickle
import csv
import sys
from itertools import islice


#python random_sim.py [n] [prob] out/school_contacts.p states.p census.p trans_prob.csv city_list.p [google_all] [matrix.out]


#setup parameter values
time_steps = 365
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

#contacts = pickle.load(open(sys.argv[3], 'rb'))

states = pickle.load(open(sys.argv[4], 'rb'))

#load census data
population = {}
census = pickle.load(open(sys.argv[5], 'rb'))
total_pop = 0
for p in census:
    total_pop += census[p]

for p in census:
    population[p] = int((census[p] / float(total_pop)) * n)

#load transition probability matrix
reader = csv.reader(open(sys.argv[6], 'rb'), delimiter=',')
T =[]
for row in reader:
    row = [(float(x) if x else 0) for x in row]
    T.append(np.array(row))

T = np.array(T)

randwriter = csv.writer(open(sys.argv[9]+'-randomT.csv', 'wb'), delimiter=',')
for r in range(0, T.shape[1]):
    row = np.random.random_sample(T.shape[0])
    row = row / float(np.sum(row))
    T[r] = row
    randwriter.writerow(row)

city_list = pickle.load(open(sys.argv[7], 'rb'))
num_cities = len(city_list)
states_to_city = {}
for c in city_list:
    city_state = c.split(',')
    ct = city_state[0]
    st = city_state[1]
    if st not in states_to_city:
        states_to_city[st] = set()
    cts = states_to_city[st]
    cts.add(ct)

google = csv.reader(open(sys.argv[8], 'rb'), delimiter=',')
g_init = list(islice(google,281))[-1]
g_init.pop(0)
g_init = [(int(x) if x else 0) for x in g_init]

Vinit = np.zeros(num_cities)
for v in g_init:
    st_index = g_init.index(v)
    state = states[st_index]
    if state in states_to_city:
        Vinit = Util.init_cities(v, Vinit, city_list, state, states_to_city[state])

print "Dictionaries loaded."

#output file
params = str(time_steps) + '-' + str(beta)
matrix = open(sys.argv[9]+"_"+params+".out", 'w')

#initialize susceptible vector
Vs = []
for i in range(num_cities):
    Vs.append(population[city_list[i]])
Vs = np.array([Vs])

#initialize latent vectors
Vl = Util.init_vectors(max_lat, num_cities)

#initialize infected vectors
Vi = Util.init_vectors(max_inf, num_cities)

print "Vectors initialized."

#initial infected city

#init_city = "New York,NY"
#init_index = city_list.index(init_city)
#init_pop = int(.001 * Vs[0,init_index])

print "Initial infected population " + str(sum(g_init))
Vs[0] -= Vinit

#determine infection period for newly infected
Vni = []
for i in range(0, max_inf):
    Vni.append( np.zeros(num_cities) )
Vni = np.array(Vni)

Vni = Util.determine_inf_pd(Vinit, Vni, max_inf)

#update infected
for i in range(len(Vi)):
    Vi[i][0] = Vni[i]

#for i in range(init_pop):
#    length = random.randint(1, max_inf)
#    v = Vi[length-1]
#    v[0,init_index] += 1

print "Initial city outbreak.. Done."
print "Begin simulation..."

t = 0
infection_matrix = []

while t < time_steps:
    infection_matrix.append(Util.state_stats(city_list,states,Vi))

    print "Spreading infection..."

    #spread infection
    Vnl = []
    for i in range(0,max_lat):
        Vnl.append( np.zeros(num_cities) )
    Vnl = np.array(Vnl)

    for i in range(len(Vi)):
        v = Vi[i]
        for r in range(v.shape[0]):
            temp = []
            for c in range(v.shape[1]):
                if v[r,c] > 0:
                    Vnl = Util.propagate(v[r,c], c, Vnl, beta, contacts, max_lat, t)
    new_latent = 0
    for i in range(0, max_lat):
        Vs[0] -= Vnl[i]
        new_latent += sum(Vnl[i])

    print "New Latent " + str(new_latent)

    print "Mobilizing agents..."

    #latents move to new city
    for i in range(len(Vl)):
        v = Vl[i]
        for r in range(v.shape[0]):
            temp = []
            for c in range(v.shape[1]):
                if v[r,c] > 0:
                    temp.append( Util.distribute(v[r,c], T[c,:]) )
            v[r] = np.sum(temp,axis=0)

    #infected move to new city
    for i in range(len(Vi)):
        v = Vi[i]
        for r in range(v.shape[0]):
            temp = []
            for c in range(v.shape[1]):
                if v[r,c] > 0:
                    temp.append( Util.distribute(v[r,c], T[c,:]) )
            v[r] = np.sum(temp,axis=0)

    print "Updating compartments..."

    #update latent
    new_infected = []
    for i in range(len(Vl)):
        v = Vl[i]
        rows = v.shape[0]
        for r in reversed(range(rows)):
            #last row becomes infected at next step
            if r == rows-1:
                new_infected.append(v[r])
            if r == 0:
                v[r] = Vnl[i]
            else:
                v[r] = v[r-1]

    new_infected = np.sum(new_infected, axis=0)

    if np.sum(new_infected) > 100000:
        sys.exit("Reached Infected # " + str(np.sum(new_infected)))

    print "New infected " + str(np.sum(new_infected))

    #determine infection period for newly infected
    Vni = []
    for i in range(0, max_inf):
        Vni.append( np.zeros(num_cities) )
    Vni = np.array(Vni)

    Vni = Util.determine_inf_pd(new_infected, Vni, max_inf)

    #update infected
    for i in range(len(Vi)):
        v = Vi[i]
        rows = v.shape[0]
        for r in reversed(range(rows)):
            if r == 0:
                v[r] = Vni[i]
            else:
                v[r] = v[r-1]

    t += 1


#write output to file
for row in infection_matrix:
    matrix.write(str(row)+'\n')

matrix.close()

print "Simulation finished."
