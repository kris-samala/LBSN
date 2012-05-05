from util import Util
import numpy as np
import fileinput
import random
import pickle
import csv
import sys

#python fast_sim.py [n] [prob] contact_dist.out states.p census.p trans_prob.csv city_list.p [matrix.out]


#setup parameter values
time_steps = 18
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
    population[p] = int((census[p] / float(total_pop)) * n)

#load transition probability matrix
reader = csv.reader(open(sys.argv[6], 'rb'), delimiter=',')
T =[]
for row in reader:
    row = [(float(x) if x else 0) for x in row]
    T.append(np.array(row))

T = np.array(T)
city_list = pickle.load(open(sys.argv[7], 'rb'))
num_cities = len(city_list)

print "Dictionaries loaded."

#output file
params = str(beta)
matrix = open(sys.argv[8]+"_"+params+".out", 'w')

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

init_city = "New York,NY"
init_index = city_list.index(init_city)
init_pop = int(.001 * Vs[0,init_index])
print "Initial infected population " + str(init_pop)
Vs[0,init_index] -= init_pop

for i in range(init_pop):
    length = random.randint(1, max_inf)
    v = Vi[length-1]
    v[0,init_index] += 1

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
                Vnl = Util.propagate(v[r,c], c, Vnl, beta, contacts, max_lat, t)

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

    print "Mobilizing agents..."

    #latents move to new city
    for i in range(len(Vl)):
        v = Vl[i]
        for r in range(v.shape[0]):
            temp = []
            for c in range(v.shape[1]):
                temp.append( Util.distribute(v[r,c], T[c,:]) )
            v[r] = np.sum(temp,axis=0)

    #infected move to new city
    for i in range(len(Vi)):
        v = Vi[i]
        for r in range(v.shape[0]):
            temp = []
            for c in range(v.shape[1]):
                temp.append( Util.distribute(v[r,c], T[c,:]) )
            v[r] = np.sum(temp,axis=0)

    t += 1


#write output to file
for row in infection_matrix:
    matrix.write(str(row)+'\n')

matrix.close()

print "Simulation finished."
