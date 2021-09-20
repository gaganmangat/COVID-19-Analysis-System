import pandas as pd
import numpy as np

def zscore_time(df, time_id):        
    df_neighbor_time = pd.read_csv('neighbor-' + time_id + '.csv')
    df_state_time = pd.read_csv('state-' + time_id + '.csv')
    
    district_id_list = []
    time_id_list = []
    neighbor_z_list = []
    state_z_list = []
    
    for i in range(df.shape[0]):
        if (df_neighbor_time.iloc[i, 3] != 0):
            zneighbor = np.around((df.iloc[i, 2] - df_neighbor_time.iloc[i, 2])/df_neighbor_time.iloc[i, 3], decimals=2)
        else:
            zneighbor = 0
        
        if (df_state_time.iloc[i, 3] != 0):    
            zstate = np.around((df.iloc[i, 2] - df_state_time.iloc[i, 2])/df_state_time.iloc[i, 3], decimals=2)
        else:
            zstate = 0
            
        district_id_list.append(df.iloc[i, 0])
        time_id_list.append(df.iloc[i, 1])
        neighbor_z_list.append(zneighbor)
        state_z_list.append(zstate)
    df_zscore = pd.DataFrame(list(zip(district_id_list, time_id_list, neighbor_z_list, state_z_list)), columns=['districtid', 'timeid', 'neighborhoodzscore', 'statezscore'])
    return df_zscore       
        
df_weekly = pd.read_csv('cases-week.csv')
df_zscore_week = zscore_time(df_weekly, 'week')
df_zscore_week.to_csv('zscore-week.csv', index=False)        
        
df_monthly = pd.read_csv('cases-month.csv')
df_zscore_month = zscore_time(df_monthly, 'month')
df_zscore_month.to_csv('zscore-month.csv', index=False)        

df_overall = pd.read_csv('cases-overall.csv')
df_zscore_overall = zscore_time(df_overall, 'overall')
df_zscore_overall.to_csv('zscore-overall.csv', index=False)        
