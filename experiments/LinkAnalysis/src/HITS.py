from path import *
from graph import *

def HubsAndAuthorities(graph, k):    
    for _ in range(k):
        # auth
        for node in graph.nodes:
            if node == None:
                continue            
            node.auth = 0
            for child_key in node.parents_nodes_key:            
                node.auth += graph.nodes[child_key].hub
            # print(f"Auth {node.vertex}'s hub:{node.hub}, auth:{node.auth}")
        # hub
        for node in graph.nodes:
            if node == None:
                continue
            
            node.hub = 0
            
            for parent_key in node.children_nodes_key:            
                node.hub += graph.nodes[parent_key].auth            
            # print(f"Hub {node.vertex}'s hub:{node.hub}, auth:{node.auth}")

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
    import argparse
    import numpy as np

    parser = argparse.ArgumentParser(description='HITS')
    parser.add_argument('--dataset', type=str, required=False,
        default='example', choices=['1', '2', '3', '4', '5', '6', 'example', 'all'],
        help='name of dataset'
    )
    parser.add_argument('--itr', type=int, default=100, help='iterator times')
    args = parser.parse_args()
    
    if args.dataset in  ['1', '2', '3', '4', '5', '6']:
        datasets = DATASETS_FILE_NAME[(int(args.dataset) - 1):int(args.dataset)]
    if args.dataset == 'all':
        datasets = DATASETS_FILE_NAME
    if args.dataset == 'example':
        datasets = DATASETS_FILE_NAME[:3]
    
    for dataset in datasets:
        print(f"Dataset:  [{dataset}]")
        dataset_file_path = get_file_path(dataset, DATASET_PATH)
        graph = read_dataset_graph(dataset_file_path)
        HubsAndAuthorities(graph, args.itr)
        hub, auth = get_result(graph)
        
        print("\033[93m", end="")
        print("Authority:")
        print(np.round(np.array(list(auth.values())), 5))
        print("Hub:")
        print(np.round(np.array(list(hub.values())), 5))
        print("\033[0m")