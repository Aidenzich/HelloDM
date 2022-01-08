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
    import argparse
    import numpy as np

    parser = argparse.ArgumentParser(description='PageRank')
    parser.add_argument('--dataset', type=str, required=False,
        default='example', choices=['1', '2', '3', '4', '5', '6', 'example', 'all'],
        help='name of dataset'
    )
    parser.add_argument('--itr', type=int, default=100, help='iterator times')
    parser.add_argument('--damping_factor', type=float, default=0.15, help='dumping factor')
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
        PageRank(graph, args.itr, args.damping_factor)
        result = get_result(graph)
        print(f"\033[93m{np.array(list(result.values()))}\033[0m")
        print()
    
    
    
