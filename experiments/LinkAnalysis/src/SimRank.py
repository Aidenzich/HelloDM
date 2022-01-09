from path import *
from graph import *
from utils import timer

def initialize_similarity_rank(graph):    
    init_similarity_matrix = []    
    node_vertexs_indices = {}

    for node in graph.nodes:
        index_count = 0
        if node == None:
            continue    
        # node_vertexs_indices.append(node.vertex)
        node_vertexs_indices[node.vertex] = index_count
        index_count += 1

    for pair_node1 in graph.nodes:
        array1d = []
        for pair_node2 in graph.nodes:
            array1d.append(1 if pair_node1 == pair_node2 else 0)
            
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
                graph.nodes[p1].vertex - 1
                ][graph.nodes[p2].vertex - 1]
    
    scale = decay_factor / (len(pair_node1.parents_nodes_key) * len(pair_node2.parents_nodes_key))
    return sim_rank_sum * scale

@timer
def SimRank(graph, k, decay_factor):    
    init_similarity_matrix, node_vertexs_indices = initialize_similarity_rank(graph)
    similarity_matrix = [[0] * len(node_vertexs_indices) for _ in range(len(node_vertexs_indices))]
    
    from tqdm import tqdm
    for _ in tqdm(range(k)):
        for pair_node1 in graph.nodes:
            if pair_node1 == None:
                continue
            for pair_node2 in graph.nodes:
                if pair_node2 == None:
                    continue
                
                similarity_matrix[pair_node1.vertex - 1] \
                    [pair_node2.vertex - 1] \
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
    from utils import init_argparse, export_score_txt
    import numpy as np

    args = init_argparse("SimRank")

    for dataset in args.datasets:
        print(f"Dataset: [{dataset}]")
        dataset_file_path = get_file_path(dataset, DATASET_PATH)        

        graph = read_dataset_graph(dataset_file_path, 
            add_edges=args.add_edges, 
            ignore_edges=args.ignore_edges
        )

        result = np.array(SimRank(graph, args.itr, args.decay_factor)[0])
        print(f"\033[93m{result}\033[0m")
        if args.save == 1:
            
            export_score_txt(result, dataset, 'SimRank')