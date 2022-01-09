from path import *
import argparse

def init_argparse(algorithm_name: str):
    parser = argparse.ArgumentParser(description=algorithm_name)
    parser.add_argument('--dataset', type=str, required=False,
        default='example', choices=['1', '2', '3', '4', '5', '6', 'example', 'all'],
        help='name of dataset.'
    )

    parser.add_argument('--itr', type=int, default=100, help='iterator times')
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

    return args