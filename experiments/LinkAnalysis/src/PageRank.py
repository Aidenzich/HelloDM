from path import *
from graph import *

def PageRank(graph, k, damping_factor):    
    for _ in range(k):
        # auth
        for node in graph.nodes:
            if node == None:
                continue            
            # node.update_pagerank(d, len(graph.nodes))
            parents = node.parents_nodes_key
                        
            page_rank_sum = sum(
                (graph.nodes[parent].page_rank / len(graph.nodes[parent].children_nodes_key) for parent in parents)
            )

            random_jumping = damping_factor / len(graph.nodes)
            node.page_rank = random_jumping + (1 - damping_factor) * page_rank_sum



def get_result(graph):
    page_rank_result = {}        
    total_pagerank_sum = 0
    
    for node in graph.nodes:
        if node == None:
            continue        
        total_pagerank_sum += node.page_rank
        
    for node in graph.nodes:
        if node == None:
            continue
        
        page_rank_result[node.vertex] = node.page_rank / total_pagerank_sum
                
    return page_rank_result

    
if __name__ == "__main__":
    import numpy as np
    for dataset in DATASETS_FILE_NAME[:3]:
        print(f"[{dataset}]")
        dataset_file_path = get_file_path(dataset, DATASET_PATH)
        graph = read_dataset_graph(dataset_file_path)
        PageRank(graph, 100, 0.15)
        result = get_result(graph)

        
                    
        
        print(f"\033[93m{np.array(list(result.values()))}\033[0m")
        print()
    
    
    
