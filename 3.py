import pandas as pd
df = pd.read_csv('neighbor-districts-id.csv')

district_name_to_id = {} #maps district name to their ids    
for i in range(df.shape[0]):
    district_name_to_id[df.iloc[i, 1]] = df.iloc[i, 0]

#create undirected graph
    
district_graph = {} #graph where every node is a district_id and an edge connects adjacent districts
#adjacency list representation is used for the graph

import ast
for i in range(df.shape[0]): 
    neigh_list = ast.literal_eval(df.iloc[i, 2]) 
    neigh_list.sort()
    temp_list = [] #list to store district names of adjacent districts
    
    for j in neigh_list: #iterate over the adjacent districts of dist
        temp_list.append(district_name_to_id[j])
    district_graph[df.iloc[i, 0]] = temp_list 
    
edges = 0    
dist_id = []
neigh_id = []

for id1 in range(101, 101 + df.shape[0]):
    for id2 in district_graph[id1]:
        dist_id.append(id1)
        neigh_id.append(id2)
        edges += 1 

df_edges = pd.DataFrame(list(zip(dist_id, neigh_id)), columns=['districtid', 'neighborid'])
df_edges.to_csv('edge-graph.csv', index=False)

