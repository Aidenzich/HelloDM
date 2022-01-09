#%%
import matplotlib.pyplot as plt
import PageRank 
import SimRank
from path import *
from graph import *
import numpy as np

def damping_factor():
    x = [ (i+1)/100 for i in range(99)]
    itr = 100
    dataset_file_path = get_file_path("graph_1.txt", DATASET_PATH)

    plt_data = {}
    # plt.style.use('dark_background')

    for _x in x:
        graph = read_dataset_graph(dataset_file_path)
        PageRank.PageRank(graph, itr, _x)
        result = PageRank.get_result(graph)
        result = np.array(list(result.values()))
        
        for idx, score in enumerate(result, start=1):
            # print(idx, score)
            if plt_data.get(idx) == None:
                plt_data[idx] = []

            plt_data[idx].append(score)
            

    for k in plt_data.keys():
        plt.plot(x, plt_data[k])
    
    plt.xlabel('damping factor')
    plt.ylabel('PageRank')    
    plt.show()    

def decay_factor():
    factors = [ (i+1)/100 for i in range(99)]
    itr = 100
    dataset_file_path = get_file_path("graph_4.txt", DATASET_PATH)

    plt_data = {}

    for f in factors:
        graph = read_dataset_graph(dataset_file_path)        
        result = np.array(SimRank.SimRank(graph, itr, f)[0])
        print(result.shape)

        for i in range(7):
            for j in range(7):
                if plt_data.get((i, j)) == None:
                    plt_data[(i, j)] = []
                plt_data[(i, j)].append(result[i][j])
        
    print(plt_data)
    for k in plt_data.keys():
        plt.plot(factors, plt_data[k])
    
    plt.xlabel('decay factor')
    plt.ylabel('SimRank')    
    plt.show()  

    

damping_factor()
decay_factor()





# %%
