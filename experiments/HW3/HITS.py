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
    graph = read_dataset_graph('./dataset/graph_3.txt')
    # graph.print_graph()
    HubsAndAuthorities(graph, 50)
    # graph.print_graph()
    hub, auth = get_result(graph)

    print("AUTH")
    print(auth)
    print("HUB")
    print(hub)


# %%
