import pandas as pd

df_portal = pd.read_csv('portal_dataframe.csv')
df_district = pd.read_csv('neighbor-districts-id.csv')

id_list = []
cases_list = []
state_list = []
time_list = []
district_list = []

for i in range(df_district.shape[0]): #iterate for all district_IDs 
    for j in range(df_portal.shape[0]): #iterate over entire confirmed cases data
        if (df_district.iloc[i, 1] == df_portal.iloc[j, 2].lower()):
            id_list.append(df_district.iloc[i, 0])
            district_list.append(df_district.iloc[i, 1])
            cases_list.append(df_portal.iloc[j, 3])
            state_list.append(df_portal.iloc[j, 1])
            time_list.append(df_portal.iloc[j, 0])
            
    
df = pd.DataFrame(list(zip(id_list, time_list, cases_list)), columns=['districtid', 'timeid', 'cases'])
#df.to_csv('cases-all.csv', index=False)

df2 = pd.DataFrame(list(zip(time_list, id_list, district_list, state_list, cases_list)), columns=['timeid','districtid', 'districtname', 'state', 'cases'])
df2.to_csv('cases-all-detailed.csv', index=False)

#______________________________________________________________________________
#import pandas as pd
#df = pd.read_csv('cases.csv')
#df2 = pd.read_csv('cases_detailed.csv')

df['timeid'] = df['timeid'].astype('datetime64[ns]') #convert the dates to datetime date

def find_cases_timeid(df, time_id, time_freq):
    date_range = pd.date_range(start='2020-03-15', end='2020-09-05', freq=time_freq) #end of week dates (Saturday)
    
    if (time_id == 'month'):
        date_range = date_range.insert(6, pd.Timestamp('2020-9-30'))
        
    date_range_id = []
    for i in range(len(date_range)):
        date_range_id.append(i+1)
    
    district_id_list = []
    time_id_list = []
    cases_id_list = []
    
    for i in range(101, 101+df_district.shape[0]):
        df_temp = df[df['districtid'] == i] #dataframe with district_id = x
        df_weekly = df_temp.resample(time_freq, label='right', closed='right', on='timeid').sum().reset_index()
        
        for j in range(len(date_range_id)):
            district_id_list.append(i)
            time_id_list.append(date_range_id[j])
            if (date_range[j] in list(df_weekly['timeid'])):
                cases_id_list.append(df_weekly[df_weekly['timeid'] == date_range[j]]['cases'].item())
            else:
                cases_id_list.append(0)
    return pd.DataFrame(list(zip(district_id_list, time_id_list, cases_id_list)), columns=['districtid', 'timeid', 'cases'])        
       
df_cases_week = find_cases_timeid(df, 'week', 'W-Sat')
df_cases_week.to_csv('cases-week.csv', index=False)

df_cases_month = find_cases_timeid(df, 'month', 'M')
df_cases_month.to_csv('cases-month.csv', index=False)


#find overall cases for every district
district_id_list = []
time_id_list = []
cases_id_list = []

for i in range(101, 101+df_district.shape[0]):
    df_temp = df[df['districtid'] == i]
    df_yearly = df_temp.resample('Y', label='right', closed='right', on='timeid').sum().reset_index()
    district_id_list.append(i)
    time_id_list.append(1)
    cases_id_list.append(df_yearly['cases'].item())

df_cases_overall = pd.DataFrame(list(zip(district_id_list, time_id_list, cases_id_list)), columns=['districtid', 'timeid', 'cases'])        
df_cases_overall.to_csv('cases-overall.csv', index=False)

    