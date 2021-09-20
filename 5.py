import pandas as pd
df_cases_detailed = pd.read_csv('cases-all-detailed.csv')

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
            #df_neigh = df_edges[df_edges['district_id'] == districtid]
            state = df_cases_detailed[df_cases_detailed['districtid'] == districtid].iloc[0]['state']
            state_districts_id = list(set(df_cases_detailed[df_cases_detailed['state'] == state]['districtid']))
            state_districts_id.remove(districtid)
            df_temp = df[df['timeid'] == i] #get all district cases for time_id i
            state_cases = []
            
            if (len(state_districts_id) == 0):
                #print(districtid)
                mean_list.append(df_temp[df_temp['districtid'] == districtid]['cases'].item())
                stdev_list.append(0)  
            else:              
                for j in state_districts_id:
                    x = df_temp[df_temp['districtid'] == j]['cases']
                    state_cases.append(x.item())        
                stdev = np.around(np.std(state_cases), decimals=2)
                mean = np.around(np.mean(state_cases), decimals=2)
                mean_list.append(mean)
                stdev_list.append(stdev)  
        
            district_id_list.append(districtid)
            time_id_list.append(i)
            
    df_states = pd.DataFrame(list(zip(district_id_list, time_id_list, mean_list, stdev_list)), columns=['districtid', 'timeid', 'statemean', 'statestdev'])
    df_states_sorted = pd.DataFrame(columns=['districtid', 'timeid', 'statemean', 'statestdev'])
    
    for i in range(101, 101+627):
        df_temp1 = df_states[df_states['districtid'] == i]
        df_states_sorted = df_states_sorted.append(df_temp1, ignore_index=True)
    
    return df_states_sorted

df_week = pd.read_csv('cases-week.csv')
df_state_week = neighbor_stats(df_week, 'week')
df_state_week.to_csv('state-week.csv', index=False)

df_month = pd.read_csv('cases-month.csv')
df_state_month = neighbor_stats(df_month, 'month')  
df_state_month.to_csv('state-month.csv', index=False) 

df_overall = pd.read_csv('cases-overall.csv')
df_state_overall = neighbor_stats(df_overall, 'overall')
df_state_overall.to_csv('state-overall.csv', index=False)