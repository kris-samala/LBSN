import networkx as nx
import matplotlib.pyplot as plt
import pickle

class LocationGraph:

    def __init__(self):
        self.graph = nx.DiGraph()

    def add_vertex(self, name):
        self.graph.add_node(name)

    def add_edge(self, node1, node2):
        if node1 != None:
            if self.graph.has_edge(node1, node2):
                self.graph[node1][node2]['weight'] += 1
            else:
                self.graph.add_edge(node1, node2, weight = 1)

    def set_coord(self, node, latd, longd):
        self.graph.add_node(node, latitude = latd, longitude = longd)

    def set_weight(self, name, weight):
        self.graph.node[name]['weight'] = weight

    def get_weight(self, name):
        return self.graph.node[name]['weight']

    def contains(self, name):
        return name in self.graph

    def neighbors(self, node):
        return self.graph.neighbors(node)

    def nodes(self):
        return self.graph.nodes()

    def get_nodes_size(self):
        return len(self.graph)

    def get_edges_size(self):
        return self.graph.size()

    def edge_weight(self, node1, node2):
        return self.graph[node1][node2]['weight']

    def total_edge_weights(self, node):
        total = 0
        for nb in self.graph.neighbors(node):
            total += self.graph[node][nb]['weight']

        return total

    def trim(self):
        low_edges = []
        for n1,n2 in self.graph.edges_iter():
            if self.graph[n1][n2]['weight'] < 10:
                low_edges.append((n1,n2))
        self.graph.remove_edges_from(low_edges)

        low_nodes = []
        for node in self.graph.nodes_iter():
            if self.graph.degree(node) < 5:
                low_nodes.append(node)
        self.graph.remove_nodes_from(low_nodes)

    def save(self, filename):
        pickle.dump(self.graph.nodes(), open(filename+"_nodes.pickle", "wb"))
        pickle.dump(self.graph.edges(data=True), open(filename+"_edges.pickle", "wb"))
        nx.write_gpickle(self.graph, filename + ".gpickle")

    def load(self, filename):
        self.graph = nx.read_gpickle(filename + ".gpickle")

    def draw(self, filename):
        nx.draw(self.graph,node_size=20,alpha=.5,with_labels=False,node_color='g',width=.3)
        plt.savefig(filename + ".png")

    def write(self, filename):
        out = open(filename, 'w')
        for node1,node2,data in self.graph.edges_iter(data=True):
            out.write(str(node1) + "\t" + str(node2) + "\t" + str(data) + "\n")
        out.close()
        nx.write_gexf(self.graph, filename+".gexf")

