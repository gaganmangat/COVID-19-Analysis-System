import pandas as pd

def spot_generator(df, time_id, method):
    if (time_id == 'week'):
        upper = 26
    elif (time_id == 'month'):
        upper = 8
    elif (time_id == 'overall'):
        upper = 2
    
    if (method == 'neighbor'):    
        df_method = pd.read_csv('neighbor-' + time_id + '.csv')
    elif (method == 'state'):
        df_method = pd.read_csv('state-' + time_id + '.csv')
        
    time_id_list = []
    spot_list = []
    district_id_list = []
    method_list = []
    
    for i in range(1, upper): #find for every week    
        df_timei = df[df['timeid'] == i]
        df_method_timei = df_method[df_method['timeid'] == i]    
        
        for j in range(df_timei.shape[0]):
            if (df_timei.iloc[j, 2] > (df_method_timei.iloc[j, 2] + df_method_timei.iloc[j, 3])):
                spot_list.append('hot')
                district_id_list.append(df_timei.iloc[j, 0])
                time_id_list.append(i)
                method_list.append(method)
            
            if (df_timei.iloc[j, 2] < (df_method_timei.iloc[j, 2] - df_method_timei.iloc[j, 3])):
                spot_list.append('cold')
                district_id_list.append(df_timei.iloc[j, 0])
                time_id_list.append(i)
                method_list.append(method)
    
    df_spots = pd.DataFrame(list(zip(time_id_list, method_list, spot_list, district_id_list)), columns=['timeid', 'method', 'spot', 'districtid'])        
    return df_spots


df_weekly = pd.read_csv('cases-week.csv')
df_spot_neighbor_week = spot_generator(df_weekly, 'week', 'neighbor')
df_spot_state_week = spot_generator(df_weekly, 'week', 'state')
df_spot_week = df_spot_neighbor_week.append(df_spot_state_week, ignore_index=True)
df_spot_week.sort_values(['timeid', 'districtid'], axis=0, ascending=True, inplace=True)
df_spot_week.to_csv('method-spot-week.csv', index=False)    

df_monthly = pd.read_csv('cases-month.csv')
df_spot_neighbor_month = spot_generator(df_monthly, 'month', 'neighbor')
df_spot_state_month = spot_generator(df_monthly, 'month', 'state')
df_spot_month = df_spot_neighbor_month.append(df_spot_state_month, ignore_index=True)
df_spot_month.sort_values(['timeid', 'districtid'], axis=0, ascending=True, inplace=True)
df_spot_month.to_csv('method-spot-month.csv', index=False)

df_overall = pd.read_csv('cases-overall.csv')
df_spot_neighbor_overall = spot_generator(df_overall, 'overall', 'neighbor')
df_spot_state_overall = spot_generator(df_overall, 'overall', 'state')
df_spot_overall = df_spot_neighbor_overall.append(df_spot_state_overall, ignore_index=True)
df_spot_overall.sort_values(['timeid', 'districtid'], axis=0, ascending=True, inplace=True)
df_spot_overall.to_csv('method-spot-overall.csv', index=False)

