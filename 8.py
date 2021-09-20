import pandas as pd

def topdistricts(df, time_id):
    time_id_list = []
    method_list = []
    spot_list = []
    district_id1_list = []
    district_id2_list = []
    district_id3_list = []
    district_id4_list = []
    district_id5_list = []
    
    if (time_id == 'week'):
        upper = 26
    elif (time_id == 'month'):
        upper = 8
    elif (time_id == 'overall'):
        upper = 2
      
    for i in range(1, upper):
        df_temp = df[df['timeid'] == i]
        
        df_largest = df_temp.nlargest(5, ['neighborhoodzscore'])
        time_id_list.append(i)
        method_list.append('neighborhood')
        spot_list.append('hot')
        
        district_id1_list.append(df_largest.iloc[0, 0])
        district_id2_list.append(df_largest.iloc[1, 0])
        district_id3_list.append(df_largest.iloc[2, 0])
        district_id4_list.append(df_largest.iloc[3, 0])
        district_id5_list.append(df_largest.iloc[4, 0])
    
        df_largest_state = df_temp.nlargest(5, ['statezscore'])
        time_id_list.append(i)
        method_list.append('state')
        spot_list.append('hot')
        district_id1_list.append(df_largest_state.iloc[0, 0])
        district_id2_list.append(df_largest_state.iloc[1, 0])
        district_id3_list.append(df_largest_state.iloc[2, 0])
        district_id4_list.append(df_largest_state.iloc[3, 0])
        district_id5_list.append(df_largest_state.iloc[4, 0])
    
        df_smallest = df_temp.nsmallest(5, ['neighborhoodzscore'])
        time_id_list.append(i)
        method_list.append('neighborhood')
        spot_list.append('cold')
        district_id1_list.append(df_smallest.iloc[0, 0])
        district_id2_list.append(df_smallest.iloc[1, 0])
        district_id3_list.append(df_smallest.iloc[2, 0])
        district_id4_list.append(df_smallest.iloc[3, 0])
        district_id5_list.append(df_smallest.iloc[4, 0])
    
        df_smallest_state = df_temp.nsmallest(5, ['statezscore'])
        time_id_list.append(i)
        method_list.append('state')
        spot_list.append('cold')
        district_id1_list.append(df_smallest_state.iloc[0, 0])
        district_id2_list.append(df_smallest_state.iloc[1, 0])
        district_id3_list.append(df_smallest_state.iloc[2, 0])
        district_id4_list.append(df_smallest_state.iloc[3, 0])
        district_id5_list.append(df_smallest_state.iloc[4, 0])
    
    df_top = pd.DataFrame(list(zip(time_id_list, method_list, spot_list, district_id1_list, district_id2_list, district_id3_list, district_id4_list, district_id5_list)), columns= ['timeid', 'method', 'spot', 'districtid1', 'districtid2', 'districtid3', 'districtid4', 'districtid5'])    
    return df_top

df_zscore_week = pd.read_csv('zscore-week.csv')
df_top_week = topdistricts(df_zscore_week, 'week')
df_top_week.to_csv('top-week.csv', index=False)

df_zscore_month = pd.read_csv('zscore-month.csv')
df_top_month = topdistricts(df_zscore_month, 'month')
df_top_month.to_csv('top-month.csv', index=False)

df_zscore_overall = pd.read_csv('zscore-overall.csv')
df_top_overall = topdistricts(df_zscore_overall, 'overall')
df_top_overall.to_csv('top-overall.csv', index=False)