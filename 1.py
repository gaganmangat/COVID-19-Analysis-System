import json

fp = open('./data_files/neighbor-districts.json')
neigh_data = json.load(fp)
fp.close()

fp = open('./data_files/data-all.json')
covid_data = json.load(fp)
fp.close()

#get the data within the range 15march to 5sept
import datetime
start_date = datetime.datetime(2020, 3, 15).date() #15 March 2020
end_date = datetime.datetime(2020, 9, 5).date() #5 September 2020
all_dates = list(covid_data.keys())

#delete the data where dates are out of range
for i in all_dates:
    this_date = datetime.datetime.strptime(i, "%Y-%m-%d").date() 
    #covid_data[this_date] = covid_data[i]
    #del covid_data[i]
    if this_date < start_date or this_date > end_date:
        del covid_data[i]

del i
del all_dates
del this_date
del start_date
del end_date        

"""   
Organization of the covid_data dictionary
dates ->| states ->| delta -> confirmed, districts -> districtnames -> delta -> confirmed
"""
date_list = []
state_list = []
district_list = []
cases_list = []

for date in covid_data.keys(): #iterates over the dates
    states = covid_data[date]
    
    for state in states.keys(): #iterates over keys (delta, districts) of state
        state_dict = states[state]
        district_dict = state_dict.get('districts')
        
        if district_dict is not None:
            for district in district_dict.keys():
                delta = district_dict[district].get('delta')
                if delta is not None:
                    if delta.get('confirmed') is not None:
                        date_list.append(date)
                        state_list.append(state)
                        district_list.append(district)
                        cases_list.append(delta.get('confirmed'))
            
#the dataframe df will contain the data-all.json data in a nice format
import pandas as pd
df = pd.DataFrame(list(zip(date_list, state_list, district_list, cases_list)), columns=['Date', 'State', 'District', 'Confirmed'])

del state_list
del date_list
del district_list
del cases_list
del delta
del state
del district_dict
del states
del date
del district
del state_dict


#______________________________________________________________________________
#rename the districts according to portal data

def rename_district(d, old_name, new_name): #d is dict, old_name and new_name are strings without Qid
    for key in d.keys():
        if key.split('/')[0] == old_name:
            old_name = old_name + '/' + key.split('/')[1]
            new_name = new_name + '/' + key.split('/')[1]
    
    d[new_name] = d[old_name]
    del d[old_name]        
    
    for key, value in d.items():
        nvalue = value.copy()
        for i in nvalue:
            if i == old_name:
                d[key].remove(i)
                if new_name not in d[key]:
                    d[key].append(new_name)

  
#make a list of old_names (neighbourdata) and new_names (portaldata).              
old_names = []
new_names = []

#remove '_' and 'district' from the district names of neighbourdata (as not used in portal data)
for i in neigh_data.keys():
    old = i.split('/')[0] #removes district id after /
    #do not add bijapur_district to the list as it will be replaced with vijayapura at a later stage
    if old == "bijapur_district":
        continue
    new = old.replace('_', ' ') #replaces _ with space
    new = new.replace(" district", "") #removes the word 'district' from string
    
    if old != new:
        old_names.append(old)
        new_names.append(new)
      
#district_matching.csv contains the mapping of old district names to new district names
df2 = pd.read_csv('./data_files/district_matching.csv')
        
for i in range(df2.shape[0]):
    old_names.append(df2.iloc[i, 2])
    new_names.append(df2.iloc[i, 1])

#rename the old names to new names in neighbour data        
for i in range(len(old_names)):
    rename_district(neigh_data, old_names[i], new_names[i])    
    
#rename the districts with same name by appending their state codes to their names    
def rename_district_qid(d, old_name, new_name): #d is dict, old_name and new_name are strings with Qid
    d[new_name] = d[old_name]
    del d[old_name]        
    
    for key, value in d.items():
        nvalue = value.copy()
        for i in nvalue:
            if i == old_name:
                d[key].remove(i)
                if new_name not in d[key]:
                    d[key].append(new_name)

rename_district_qid(neigh_data, "aurangabad/Q43086", "aurangabad_br/Q43086")
rename_district_qid(neigh_data, "aurangabad/Q592942", "aurangabad_mh/Q592942")
rename_district_qid(neigh_data, "balrampur/Q16056268", "balrampur_ct/Q16056268")
rename_district_qid(neigh_data, "balrampur/Q1948380", "balrampur_up/Q1948380")
rename_district_qid(neigh_data, "bilaspur/Q100157", "bilaspur_ct/Q100157")
rename_district_qid(neigh_data, "bilaspur/Q1478939", "bilaspur_hp/Q1478939")
rename_district_qid(neigh_data, "hamirpur/Q2019757", "hamirpur_up/Q2019757")
rename_district_qid(neigh_data, "hamirpur/Q2086180", "hamirpur_hp/Q2086180")
rename_district_qid(neigh_data, "pratapgarh/Q1473962", "pratapgarh_up/Q1473962")
rename_district_qid(neigh_data, "pratapgarh/Q1585433", "pratapgarh_rj/Q1585433")

#Also change name of above districts on portal dataframe and also update districts of states with no district data as state_district
t = 0
for i in range(df.shape[0]):
    if (df.iloc[i, 2].lower() == 'aurangabad'):
        t += 1
        if (df.iloc[i, 1] == 'BR'):
            df.iloc[i, 2] = df.iloc[i, 2] + '_' + 'BR'
        elif (df.iloc[i, 1] == 'MH'):
            df.iloc[i, 2] = df.iloc[i, 2] + '_' + 'MH'
        else:
            print(df.iloc[i, 2], df.iloc[i, 1])
    elif (df.iloc[i, 2].lower() == 'balrampur'):
        t += 1
        if (df.iloc[i, 1] == 'CT'):
            df.iloc[i, 2] = df.iloc[i, 2] + '_' + 'CT'
        elif (df.iloc[i, 1] == 'UP'):
            df.iloc[i, 2] = df.iloc[i, 2] + '_' + 'UP'
        else:
            print(df.iloc[i, 2], df.iloc[i, 1])  
    elif (df.iloc[i, 2].lower() == 'bilaspur'):
        t += 1
        if (df.iloc[i, 1] == 'CT'):
            df.iloc[i, 2] = df.iloc[i, 2] + '_' + 'CT'
        elif (df.iloc[i, 1] == 'HP'):
            df.iloc[i, 2] = df.iloc[i, 2] + '_' + 'HP'
        else:
            print(df.iloc[i, 2], df.iloc[i, 1])   
    elif (df.iloc[i, 2].lower() == 'hamirpur'):
        t += 1
        if (df.iloc[i, 1] == 'UP'):
            df.iloc[i, 2] = df.iloc[i, 2] + '_' + 'UP'
        elif (df.iloc[i, 1] == 'HP'):
            df.iloc[i, 2] = df.iloc[i, 2] + '_' + 'HP'
        else:
            print(df.iloc[i, 2], df.iloc[i, 1])   
    elif (df.iloc[i, 2].lower() == 'pratapgarh'):
        t += 1
        if (df.iloc[i, 1] == 'UP'):
            df.iloc[i, 2] = df.iloc[i, 2] + '_' + 'UP'
        elif (df.iloc[i, 1] == 'RJ'):
            df.iloc[i, 2] = df.iloc[i, 2] + '_' + 'RJ'
        else:
            print(df.iloc[i, 2], df.iloc[i, 1])   
    elif (df.iloc[i, 2].lower() == 'unknown'):
        t += 1
        if (df.iloc[i, 1] == 'TG'):
            df.iloc[i, 2] = 'telengana_district'
        elif (df.iloc[i, 1] == 'AS'):
            df.iloc[i, 2] = 'assam_district'
        elif (df.iloc[i, 1] == 'MN'):
            df.iloc[i, 2] = 'manipur_district'
        elif (df.iloc[i, 1] == 'SK'):
            df.iloc[i, 2] = 'sikkim_district'
        elif (df.iloc[i, 1] == 'GA'):
            df.iloc[i, 2] = 'goa_district'
            

df.to_csv('portal_dataframe.csv', index=None)
    
#______________________________________________________________________________

#Merge the required districts
def merge_districts(d, new_name, old_names): #d is dictionary, new_name is string, old_names is list
    district_id = []
    for name in old_names:
        district_id.append(int(name.split('Q')[1]))
    district_id = min(district_id) #min of those IDs
    new_name = new_name + '/Q' + str(district_id) 
    
    #find neighbours of new_name (all neighbours of old_names)
    neighbours = []
    for key, value in d.items():
        if key in old_names: 
            for i in value: #copy the neighbour list
                if i not in neighbours:
                    neighbours.append(i)    
    #remove old_names from neighbours if any
    for name in old_names:
        if name in neighbours:
            neighbours.remove(name)   
    #create new entry
    d[new_name] = neighbours                        
    #delete old_names entries
    for i in old_names:
        del d[i]                        
    #replace old_names with new_name in entire dictionary    
    for key, value in d.items():
        nvalue = value.copy() #copy list of values to nvalue
        for i in nvalue:
            if i in old_names:
                #print("key: ", key)
                #print("value: ", value)
                #print("i ", i)
                d[key].remove(i)
                if new_name not in d[key]:
                    d[key].append(new_name)
                    
#merge delhi districts into one
delhi = []
for district in neigh_data.keys():
    if 'delhi' in district:
        delhi.append(district)        
merge_districts(neigh_data, 'delhi', delhi)

#merge mumbai_suburban and mumbai_city to mumbai
mumbai = []
for district in neigh_data.keys():
    if 'mumbai' in district:
        mumbai.append(district)        
merge_districts(neigh_data, 'mumbai', mumbai)

#merge the following states districts into one since they have no districts data on portal
telengana = []
assam = []
goa = []
manipur = []
sikkim = []
others = [] 
#others will contain the other districts which have no cases from the portal and hence can be removed from the neighbourdata file

#the below file contains the data of all districts present in neighbourdata file and not present on portal
notmatchedneighbourdf = pd.read_csv('./data_files/notmatchedneighbourdistricts.csv', header=None)

for i in range(notmatchedneighbourdf.shape[0]):
    if ('TG' in notmatchedneighbourdf.iloc[i, 1]):
        telengana.append(notmatchedneighbourdf.iloc[i, 0])
        
    elif ('AS' in notmatchedneighbourdf.iloc[i, 1]):
        assam.append(notmatchedneighbourdf.iloc[i, 0])
        
    elif ('GA' in notmatchedneighbourdf.iloc[i, 1]):
        goa.append(notmatchedneighbourdf.iloc[i, 0])
        
    elif ('MN' in notmatchedneighbourdf.iloc[i, 1]):
        manipur.append(notmatchedneighbourdf.iloc[i, 0])
        
    elif ('SK' in notmatchedneighbourdf.iloc[i, 1]):
        sikkim.append(notmatchedneighbourdf.iloc[i, 0])
    else:
        others.append(notmatchedneighbourdf.iloc[i, 0])

#the following lists will contain the above districts appended with their Qids so they can be passed to the merge_districts function
telengana_id = []
assam_id = []
goa_id = []
manipur_id = []
sikkim_id = []
others_id = []

for i in neigh_data.keys():
    j = i.split('/')[1]
    i = i.split('/')[0] #removes district id after /
    i = i.replace('_', ' ') #replaces _ with space
    i = i.replace(" district", "") #removes the word 'district' from string
    
    if (i in telengana):
        telengana_id.append(i + '/' + j)
    elif (i in assam):
        assam_id.append(i + '/' + j)
    elif (i in goa):
        goa_id.append(i + '/' + j)
    elif (i in manipur):
        manipur_id.append(i + '/' + j)
    elif (i in sikkim):
        sikkim_id.append(i + '/' + j)
    elif (i in others):
        others_id.append(i + '/' + j)      
del i
        
merge_districts(neigh_data, 'telengana_district', telengana_id)
merge_districts(neigh_data, 'assam_district', assam_id)
merge_districts(neigh_data, 'goa_district', goa_id)
merge_districts(neigh_data, 'manipur_district', manipur_id)
merge_districts(neigh_data, 'sikkim_district', sikkim_id)        
        
#______________________________________________________________________________

#delete the districts present in neighbourdata and have no confirmed cases on portal (total of 9 such districts)
#they are present in the other_id list

def delete_districts(d, district_names): 
    for district in district_names:
        #print(district)
        #delete the entries where 'district' is a neighbour of some other district
        #delete 'district' from entires of all its neighbours
        for neighbour in d[district]:
            d[neighbour].remove(district)
        #now delete the district entry 
        del d[district]

delete_districts(neigh_data, others_id)

#______________________________________________________________________________

#find the list of all portal districts and states        
portal_districts = []
portal_states = []
for i in range(df.shape[0]):
    if df.iloc[i, 2] == 'Unknown':
        continue
    if df.iloc[i, 2].lower() not in portal_districts:
        portal_districts.append(df.iloc[i, 2].lower())
        portal_states.append(df.iloc[i, 1])

del i

#find the list of all neighbourdata districts
file_districts = []
for i in neigh_data.keys():
    i = i.split('/')[0] #removes district id after /
    if i not in file_districts:
        file_districts.append(i)        
del i

#find the neighbourdata districts which are not present on the portal
matched = []
not_matched = []    

for i in file_districts:
    if i in portal_districts:
        matched.append(i)
    else:
        not_matched.append(i)
    
#find the portaldistricts not present in neighbourdata districts
matchedcton = []
not_matchedcton = []
matchedcton_states = []
not_matchedcton_states = []
for i in range(len(portal_districts)):
    if portal_districts[i] in file_districts:
        matchedcton.append(portal_districts[i])
        matchedcton_states.append(portal_states[i])
    else:
        not_matchedcton.append(portal_districts[i])
        not_matchedcton_states.append(portal_states[i])
        
dfnotmatchedcton = pd.DataFrame(list(zip(not_matchedcton, not_matchedcton_states)), columns = ['District', 'State'])
        
#write the modified neighbourdata file to json
with open("neighbor-districts-modified.json", "w") as file:
    json.dump(neigh_data, file)

#sort according to district names and give them ids starting from 101
district_name = list(neigh_data.keys())
district_neigh = list(neigh_data.values())

for i in range(len(district_name)):
    district_name[i] = district_name[i].split('/')[0]
    
for nlist in district_neigh:
    for i in range(len(nlist)):
        nlist[i] = nlist[i].split('/')[0]
        
ids = []
for i in range(101, 101 + len(district_name)):
    ids.append(i)
    
import pandas as pd
df3 = pd.DataFrame(list(zip(district_name, district_neigh)), columns=['districtname', 'districtneighbors'])
df3 = df3.sort_values(by='districtname')

df3.insert(loc=0, column='districtid', value=ids)
df3.to_csv('neighbor-districts-id.csv', index=False)
