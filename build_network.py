import sys
import fileinput
import itertools
import pickle
from locations import LocationGraph

#python build_network.py out/user_checkins.out out/coordinates.p out/gowalla_net

#users = pickle.load(open("out/" + sys.argv[1], "rb"))
users = {}
coords = pickle.load(open(sys.argv[2], "rb"))
out = sys.argv[3]
Gowalla = LocationGraph()
fmt = "%Y-%m-%d %H:%M:%S"


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
