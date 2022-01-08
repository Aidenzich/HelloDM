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
    graph = read_dataset_graph('./dataset/graph_4.txt')    
    
    print(SimRank(graph, 100, 0.9)[0])