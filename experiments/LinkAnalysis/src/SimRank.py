from path import *
from graph import *

def initialize_similarity_rank(graph):    
    """[summary]
    Args:
        graph ([type]): [description]

    Returns:
        list: similarity_matrix
        [
            [1, 0, 0, 0, 0], 
            [0, 1, 0, 0, 0], 
            [0, 0, 1, 0, 0], 
            [0, 0, 0, 1, 0], 
            [0, 0, 0, 0, 1]
        ],
        list: node_vertexs_indices
        [
            1, 2, 3, 4
        ]
    """
    init_similarity_matrix = []
    
    node_vertexs_indices = []
    for node in graph.nodes:
        if node == None:
            continue    
        node_vertexs_indices.append(node.vertex)
    
    
    for pair_node1 in graph.nodes:
        array1d = []
        for pair_node2 in graph.nodes:
            if (pair_node1 == pair_node2):
                array1d.append(1)
            else:
                array1d.append(0)
        init_similarity_matrix.append(array1d)
    
    return init_similarity_matrix, node_vertexs_indices

def calculate_similarity_rank_sum(graph, pair_node1, pair_node2, 
                                  init_similarity_matrix, node_vertexs_indices, 
                                  decay_factor):
    sim_rank_sum = 0
    if pair_node1.vertex == pair_node2.vertex:
        sim_rank_sum = 1
        return sim_rank_sum
    
    if len(pair_node1.parents_nodes_key) == 0 or len(pair_node2.parents_nodes_key) == 0:
        return sim_rank_sum
    
    
    for p1 in pair_node1.parents_nodes_key:
        for p2 in pair_node2.parents_nodes_key:
            sim_rank_sum +=  init_similarity_matrix[
                node_vertexs_indices.index(graph.nodes[p1].vertex)
                ][
                node_vertexs_indices.index(graph.nodes[p2].vertex)
                ]
    
    scale = decay_factor / (len(pair_node1.parents_nodes_key) * len(pair_node2.parents_nodes_key))
    return sim_rank_sum * scale


def SimRank(graph, k, decay_factor):
    init_similarity_matrix, node_vertexs_indices = initialize_similarity_rank(graph)
    similarity_matrix = [[0] * len(node_vertexs_indices) for _ in range(len(node_vertexs_indices))]
        
    for _ in range(k):
        for pair_node1 in graph.nodes:
            if pair_node1 == None:
                continue
            for pair_node2 in graph.nodes:
                if pair_node2 == None:
                    continue
                # sim_rank = 
                similarity_matrix[node_vertexs_indices.index(pair_node1.vertex)] \
                    [node_vertexs_indices.index(pair_node2.vertex)] \
                    = calculate_similarity_rank_sum(
                        graph,
                        pair_node1 = pair_node1, pair_node2 = pair_node2, 
                        init_similarity_matrix = init_similarity_matrix, 
                        node_vertexs_indices = node_vertexs_indices, 
                        decay_factor = decay_factor
                    )
        init_similarity_matrix = similarity_matrix
    return similarity_matrix, node_vertexs_indices
                

if __name__ == "__main__":
    import argparse
    import numpy as np

    parser = argparse.ArgumentParser(description='HITS')
    parser.add_argument('--dataset', type=str, required=False,
        default='example', choices=['1', '2', '3', '4', '5', '6', 'example', 'all'],
        help='name of dataset'
    )
    parser.add_argument('--itr', type=int, default=50, help='iterator times')
    args = parser.parse_args()
    
    if args.dataset in  ['1', '2', '3', '4', '5', '6']:
        datasets = DATASETS_FILE_NAME[(int(args.dataset) - 1):int(args.dataset)]
    if args.dataset == 'all':
        datasets = DATASETS_FILE_NAME
    if args.dataset == 'example':
        datasets = DATASETS_FILE_NAME[:3]

    
    for dataset in datasets:    
        print(f"Dataset: [{dataset}]")
        dataset_file_path = get_file_path(dataset, DATASET_PATH)
        graph = read_dataset_graph(dataset_file_path)
        print(f"\033[93m{np.array(SimRank(graph, 100, 0.9)[0])}\033[0m")