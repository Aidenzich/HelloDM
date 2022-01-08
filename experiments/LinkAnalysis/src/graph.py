from path import *

# A Graph is composed of several points (vertex) 
# and several edges
class Node:
    def __init__(self, data):
        self.vertex = data
        self.auth = 1
        self.hub = 1
        self.page_rank = 1
        self.children_nodes_key = []
        self.parents_nodes_key = []

class Graph:
    def __init__(self, vertices):
        self.vertices_num = vertices
        self.nodes = [None] * self.vertices_num

    def add_edge(self, source, destination):
        # Add source node
        if self.nodes[source] == None:
            self.nodes[source] = Node(source)
        
        if self.nodes[destination] == None:
            self.nodes[destination] = Node(destination)
                        
        self.nodes[source].children_nodes_key.append(destination)
        self.nodes[destination].parents_nodes_key.append(source)

    def print_graph(self):
        for v in range(self.vertices_num):
            if v == 0 or self.nodes[v] == None:
                continue
                                    
            v_node = self.nodes[v]
            print(v, end="")            
            for c_key in v_node.children_nodes_key:
                print(f" -> {self.nodes[c_key].vertex}", end="")
            
            print(f"\n(hub:{v_node.hub}, auth:{v_node.auth})")
            print("\n")

def read_dataset_graph(filename):        
    with open(filename) as f:
        rows = f.readlines()
    total_nodes = []
    edges = []
    for r in rows:
        # strip = Remove spaces at the beginning and at the end of the string
        r = r.strip().split(',')
        r = [int(i) for i in r ]
        edges.append(r)
        total_nodes += r        
    total_nodes = list(set(total_nodes))
    
    graph = Graph(len(total_nodes)+1)
    for e in edges:        
        graph.add_edge(e[0], e[1])
    
    return graph

if __name__ == "__main__":
    V = 5
    graph = Graph(V)    
    graph.add_edge(0, 1)
    graph.add_edge(0, 4)
    graph.add_edge(1, 2)
    graph.add_edge(1, 3)
    graph.add_edge(1, 4)
    graph.add_edge(2, 3)
    graph.add_edge(3, 4)

    graph.print_graph()