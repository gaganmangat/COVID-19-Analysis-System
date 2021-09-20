import pandas as pd

df_cases_detailed = pd.read_csv('cases_detailed.csv')
state_list = list(set(df_cases_detailed['state'].tolist()))
state_list.sort()
cases_list = []

for state in state_list:
    cases_list.append(df_cases_detailed[df_cases_detailed['state'] == state]['confirmed_cases'].sum())


df_state_cases = pd.DataFrame(list(zip(state_list, cases_list)), columns=['state', 'cases'])

df_state_cases.sort_values(['cases'], axis=0, inplace=True)