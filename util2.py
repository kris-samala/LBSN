import numpy as np
import random
import math

class Util:

    @staticmethod
    def state_stats(city_list, states, inf_vectors):
        infected = {}
        s = [0]*50

        for i in range(len(inf_vectors)):
            v = inf_vectors[i]
            for r in range(v.shape[0]):
                for c in range(v.shape[1]):
                    loc = city_list[c]
                    state = loc.split(',')[1]
                    if v[r,c] > 0:
                        if state in infected:
                            infected[state] += v[r,c]
                        else:
                            infected[state] = v[r,c]

        for state in infected:
            index = states.index(state)
            s[index] = infected[state]

        return s

    @staticmethod
    def distribute(num, prob_dist):
        num = int(num)
        cum_sum = np.cumsum(prob_dist)
        dist = np.zeros(len(prob_dist))
        for i in range(num):
            r = random.random()
            for j in range(len(cum_sum)):
                if cum_sum[j] >= r:
                    dist[j] += 1
                    break
        return dist

    @staticmethod
    def det_distribute(num, prob_dist):
        dist = num*prob_dist

        return dist


    @staticmethod
    def init_vectors(max_pd, num_cities):
        V = []
        for i in range(1,max_pd+1):
            V.append( np.zeros((i,num_cities)) )

        return V

    @staticmethod
    def infect_indiv(p):
        rand = random.random()
        return rand <= p

    @staticmethod
    def seasonal_prob(p, t):
        a = .6
        omega = .009
        phi = 1.87
        lamda = .55
        return p * (a*math.pow(math.fabs(math.sin(omega*t)),lamda))


    @staticmethod
    def propagate(n, city, V, prob, contacts, max_lat, tstep):
        p = Util.seasonal_prob(prob, tstep)
        for i in range(int(n)):
            c = contacts[ random.randint(0,len(contacts)-1) ]
            for i in range(c):
                if Util.infect_indiv(p):
                    pd = random.randint(0,max_lat-1)
                    V[pd][city] += 1
        return V

    @staticmethod
    def determine_inf_pd(infected, V, max_inf):
        for i in range(len(infected)):
            num = int(infected[i])
            if num > 0:
                for j in range(num):
                    pd = random.randint(0,max_inf-1)
                    V[pd][i] += 1

        return V

    @staticmethod
    def init_cities(v, V, city_list, state, city_choices):
        for i in range(v):
            r = random.choice(list(city_choices))
            loc = r + ',' + state
            index = city_list.index(loc)
            V[index] += 1

        return V


