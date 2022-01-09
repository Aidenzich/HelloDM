from path import *
from graph import *

def PageRank(graph, k, damping_factor):    
    for _ in range(k):        
        for node in graph.nodes:
            if node == None:
                continue            
            
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
    from utils import init_argparse, export_score_txt
    import numpy as np
    args = init_argparse("PageRank")
    
    for dataset in args.datasets:
        print(f"Dataset: [{dataset}]")
        dataset_file_path = get_file_path(dataset, DATASET_PATH)
        
        graph = read_dataset_graph(dataset_file_path, 
            add_edges=args.add_edges, 
            ignore_edges=args.ignore_edges
        )

        PageRank(graph, args.itr, args.damping_factor)
        result = get_result(graph)
        result = np.array(list(result.values()))
        print(f"\033[93m{result}\033[0m")
        print()
        if args.save == 1:
            from utils import export_score_txt
            export_score_txt(result, dataset, 'PageRank')
        
