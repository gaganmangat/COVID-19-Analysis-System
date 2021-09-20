import pandas as pd
df_edges = pd.read_csv('edge-graph.csv')

import numpy as np
def neighbor_stats(df, time_id):
    if (time_id == 'week'):
        upper = 26
    elif (time_id == 'month'):
        upper = 8
    elif (time_id == 'overall'):
        upper = 2
        
    district_id_list = []
    time_id_list = []
    mean_list = []
    stdev_list = []
    
    for i in range(1, upper):
        for districtid in range(101, 101 + 627):
            df_neigh = df_edges[df_edges['districtid'] == districtid]
            df_temp = df[df['timeid'] == i] #get all district cases for time_id i
            neighbors = df_neigh['neighborid'].tolist()
            neighbor_cases = []
            
            for j in neighbors:
                x = df_temp[df_temp['districtid'] == j]['cases']
                neighbor_cases.append(x.item())
                
            stdev = np.around(np.std(neighbor_cases), decimals=2)
            mean = np.around(np.mean(neighbor_cases), decimals=2)
            district_id_list.append(districtid)
            time_id_list.append(i)
            mean_list.append(mean)
            stdev_list.append(stdev)  
        
    df_neighbor = pd.DataFrame(list(zip(district_id_list, time_id_list, mean_list, stdev_list)), columns=['districtid', 'timeid', 'neighbormean', 'neighborstdev'])
    df_neighbor_sorted = pd.DataFrame(columns=['districtid', 'timeid', 'neighbormean', 'neighborstdev'])
    
    for i in range(101, 101+627):
        df_temp1 = df_neighbor[df_neighbor['districtid'] == i]
        df_neighbor_sorted = df_neighbor_sorted.append(df_temp1, ignore_index=True)
    
    return df_neighbor_sorted

df_week = pd.read_csv('cases-week.csv')
df_neighbor_week = neighbor_stats(df_week, 'week')
df_neighbor_week.to_csv('neighbor-week.csv', index=False)

df_month = pd.read_csv('cases-month.csv')
df_neighbor_month = neighbor_stats(df_month, 'month')  
df_neighbor_month.to_csv('neighbor-month.csv', index=False) 

df_overall = pd.read_csv('cases-overall.csv')
df_neighbor_overall = neighbor_stats(df_overall, 'overall')
df_neighbor_overall.to_csv('neighbor-overall.csv', index=False)
    
    
    
    
 