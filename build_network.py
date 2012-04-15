import sys
import fileinput
import itertools
import pickle
from locations import LocationGraph

#python build_network.py out/user_checkins.out out/austin.out out/coordinates.p out/gowalla_net

#users = pickle.load(open("out/" + sys.argv[1], "rb"))
users = {}
austin = {}
coords = pickle.load(open(sys.argv[3], "rb"))
out = sys.argv[4]
Gowalla = LocationGraph()
fmt = "%Y-%m-%d %H:%M:%S"

austin_weight = .24
epsilon = 1

if len(sys.argv) < 2:
    print "Filename required"
else:
    for line in fileinput.input(sys.argv[1]):
        line = line.split("|")
        u = line.pop(0)
        users[u] = []
        while len(line) > 0:
            entry = line.pop(0)
            entry = entry.split(">")
            l = users[u]
            l.append(entry[0])
            users[u] = l

    for u in users:
        locs = users[u]
        prev = None
        for city in locs:
            Gowalla.add_edge(prev, city)
            prev = city

#Austin walkers
    for line in fileinput.input(sys.argv[2]):
        line = line.split("|")
        u = line.pop(0)
        austin[u] = []
        while len(line) > 0:
            entry = line.pop(0)
            entry = entry.split(">")
            l = austin[u]
            l.append(entry[0])
            austin[u] = l
#assign .5 weight for each edge walk
    for u in austin:
        locs = austin[u]
        prev = None
        for city in locs:
            Gowalla.add_edge(prev, city, austin_weight)
            prev = city

#add epsilon weight between all pairs of nodes
    Gowalla.make_connected(epsilon)

#    for line in fileinput.input(sys.argv[1]):
#        line = line.rstrip()
#        line = line.split("\t")
#        userID = line.pop(0)
#
#        for city1, city2 in itertools.combinations(line,2):
#            Gowalla.add_edge(city1, city2)

#    Gowalla.graph.remove_node("NULL,NULL")
#    Gowalla.trim()

    for node in Gowalla.nodes():
        latd, longd = coords[node]
        Gowalla.set_coord(node, latd, longd)

    Gowalla.save(out)
#    Gowalla.draw(sys.argv[3])

loadedGraph = LocationGraph()
loadedGraph.load(out)

loadedGraph.write(out)

stats = open(out+".stats", 'w')
stats.write("Gowalla Network Summary")
stats.write("\nNodes: " + str(Gowalla.get_nodes_size()))
stats.write("\nEdges: " + str(Gowalla.get_edges_size()))
stats.close()
