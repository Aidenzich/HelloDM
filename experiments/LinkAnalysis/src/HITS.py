from path import *
from graph import *


def HubsAndAuthorities(graph, k):    
    for _ in range(k):
        # Calculate auth
        for node in graph.nodes:
            if node == None:
                continue            
            node.auth = 0
            
            # The sum of the hub of its parents nodes.
            for p_key in node.parents_nodes_key:
                node.auth += graph.nodes[p_key].hub
            
        # Calculate hub
        for node in graph.nodes:
            if node == None:
                continue
            
            node.hub = 0
            
            # The sum of the authority of its children nodes.
            for c_key in node.children_nodes_key:            
                node.hub += graph.nodes[c_key].auth            
            

def get_result(graph):
    hub_result = {}
    auth_result = {}
    hub_sum = 0
    auth_sum = 0
    for v in range(graph.vertices_num):
        if v == 0 or graph.nodes[v] == None:
            continue
        v_node = graph.nodes[v]
    
        hub_result[v_node.vertex] = v_node.hub
        hub_sum+= v_node.hub
        auth_result[v_node.vertex] = v_node.auth
        auth_sum+= v_node.auth
    
    for v in hub_result.keys():
        hub_result[v] = hub_result[v] / hub_sum
        auth_result[v] = auth_result[v] / auth_sum
    
    return hub_result, auth_result



if __name__ == "__main__":    
    import numpy as np
    from utils import init_argparse, export_score_txt
    
    args = init_argparse("HITS")
    
    for dataset in args.datasets:
        print(f"Dataset:  [{dataset}]")
        dataset_file_path = get_file_path(dataset, DATASET_PATH)
        
        graph = read_dataset_graph(dataset_file_path, 
            add_edges=args.add_edges, 
            ignore_edges=args.ignore_edges
        )

        HubsAndAuthorities(graph, args.itr)
        hub, auth = get_result(graph)
        auth = np.round(np.array(list(auth.values())), 8) 
        hub = np.round(np.array(list(hub.values())), 8)
        print("\033[93m", end="")
        print("Authority:")
        print(auth)
        print("Hub:")
        print(hub)
        print("\033[0m")

        if args.save == 1:
            from utils import export_score_txt
            export_score_txt(auth, dataset, 'Authority')
            export_score_txt(hub, dataset, 'Hub')