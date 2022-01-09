from path import *
import argparse
import numpy as np 
def init_argparse(algorithm_name: str):
    parser = argparse.ArgumentParser(description=algorithm_name)
    parser.add_argument('--dataset', type=str, required=False,
        default='example', choices=['1', '2', '3', '4', '5', '6', 'example', 'all', 'ibm'],
        help='name of dataset.'
    )

    parser.add_argument('--itr', type=int, default=100, help='iterator times')

    parser.add_argument('--save', type=int, default=1, choices=[0,1],
        help="0: Don't save result, 1: Save result")

    parser.add_argument('--add_edges', nargs='+', default=[], 
        help='Create new edge to Graph.')

    parser.add_argument('--ignore_edges', nargs='+', default=[],
        help='Edge that want to ignore from Graph.')



    if algorithm_name == "PageRank":
        parser.add_argument('--damping_factor', type=float, default=0.15, help='set dumping factor')
    if algorithm_name == "SimRank":
        parser.add_argument('--decay_factor', type=float, default=0.9, help='set decay factor')

    args = parser.parse_args()

    if args.add_edges != None:
        args.add_edges = [[int(elem) for elem in edge_str.split(',')] for edge_str in args.add_edges]

    if args.ignore_edges != None:
        args.ignore_edges = [[int(elem) for elem in edge_str.split(',')] for edge_str in args.ignore_edges]
    
    if args.dataset in  ['1', '2', '3', '4', '5', '6']:
        args.datasets = DATASETS_FILE_NAME[(int(args.dataset) - 1):int(args.dataset)]

    if args.dataset == 'all':
        args.datasets = DATASETS_FILE_NAME

    if args.dataset == 'example':
        args.datasets = DATASETS_FILE_NAME[:3]

    if args.dataset == 'ibm':
        args.datasets = ['ibm.txt']
    return args


def export_score_txt(numpy_array: np.array, graph_name: str, score_name: str):
    graph_name = graph_name.replace('.txt', '')
    export_path = get_file_path(f"{graph_name}_{score_name}.txt", f"exports/{graph_name}")
    if score_name == "SimRank":
        np.savetxt(export_path, numpy_array, fmt='%1.5f', delimiter=" ", newline="\n")
    else:
        np.savetxt(export_path, numpy_array, fmt='%1.5f', delimiter=" ", newline=" ")