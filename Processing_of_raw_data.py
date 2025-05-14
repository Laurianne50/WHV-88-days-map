'''Aim of the code: create a DB of Australian postal codes in which WHV can work towards their 88 days'''

import pandas as pd

'''
Data are manually extracted from the Australian GOV website 
(https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-listing/work-holiday-417/specified-work)
Relevant data are tables 1 to 6
Data was collected on April 14, 2025
'''

raw_gov_website = pd.read_csv('C:/Users/Proprietaire/Desktop/Code/Australia_map/Raw_data.txt', sep='\t')

''' Several types of data in table: 
- Type 1: 'All postcodes in ACT are eligible' --> in that case, post codes have to be retrieved manually for each state
- Type 2: '2224 to 2234' --> in that case, post codes have to be completed
- Type 3: '2083, 2172, 2173, 2178'
WARNING: Post codes at the frontier between two states can overlap (ex: 0872 is found in both SA and NT)
'''

# Retrieved Type 1 data
raw_gov_website_All = raw_gov_website[raw_gov_website['Postcode'].str.contains('All')]
raw_gov_website_All = raw_gov_website_All.drop(["Postcode"], axis=1)

# Homogenize States Names
dictionnary_states = {
    "state": ["NT", "SA", "TAS", "Norfolk Island", "ACT", "WA", "NSW", "QLD", "VIC"],
    "State/Territory": ["Northern Territory", "South Australia", 
            "Tasmania", "Norfolk Island", "Australian Capital Territory (ACT)",
            "Western Australia", "New South Wales", "Queensland", "Victoria"]
}
table_titles_state = pd.DataFrame(dictionnary_states)
raw_gov_website_All = pd.merge(raw_gov_website_All, table_titles_state, on="State/Territory")

'''Australian Postcodes are retrieved from https://github.com/matthewproctor/australianpostcodes/tree/master'''
australian_postcodes_file = pd.read_csv('C:/Users/Proprietaire/Desktop/Code/Australia_map/australian_postcodes.csv', sep=',')
raw_gov_website_All_2 = pd.merge(raw_gov_website_All, australian_postcodes_file, on="state")
raw_gov_website_All_2 = raw_gov_website_All_2[["State/Territory", "Table number", "postcode"]]\
    .rename(columns={"postcode": "Postcode"}).drop_duplicates()

# Retrieved Type 2 and 3 data
raw_data = raw_gov_website[~raw_gov_website['Postcode'].str.contains('All')]

# Edit Type 2 data
raw_to = raw_data[raw_data['Postcode'].str.contains('to')]
raw_to['Postcode'] = raw_to['Postcode'].str.split(',')
raw_to = raw_to.explode('Postcode')

# Edit Type 3 data
raw_to_1 = raw_to[~raw_to['Postcode'].str.contains('to')]
raw_to_1['Postcode'] = raw_to_1['Postcode'].str.split(',')
raw_to_1 = raw_to_1.explode('Postcode')

raw_to_noTo = raw_data[~raw_data['Postcode'].str.contains('to')]
raw_to_noTo['Postcode'] = raw_to_noTo['Postcode'].str.split(',')
raw_to_noTo = raw_to_noTo.explode('Postcode')

# Assemble the data
raw_to_add_back = pd.concat([raw_to_noTo, raw_to_1]) # to add back to the full table

raw_to_2 = raw_to[raw_to['Postcode'].str.contains('to')]
raw_to_split = raw_to_2['Postcode'].str.rsplit(' to ', expand=True) #problem
raw_to_3 = pd.merge(raw_to_2, raw_to_split, left_index=True, right_index=True)\
    .drop(["Postcode"], axis=1).drop_duplicates().reset_index()
raw_to_3[0] = pd.to_numeric(raw_to_3[0], errors='coerce')
raw_to_3[1] = pd.to_numeric(raw_to_3[1], errors='coerce')

list_test = []
for x in list(range(0,len(raw_to_3))):
    t = list(range(raw_to_3[0][x], raw_to_3[1][x]+1))
    list_test.append(t)
raw_to_3["Postcode"] = list_test
raw_to_3 = raw_to_3.explode('Postcode').drop([0,1,'index'], axis=1)

'''Assemble tables'''
cleaned_data = pd.concat([raw_to_add_back,raw_to_3, raw_gov_website_All_2])\
    .reset_index().drop(['index'], axis=1)

# Homogenize Tables Titles
dictionnary_tablesTitles_gov_website = {
    "Table number": [1, 2, 3, 4, 5, 6],
    "Title": ["Remote and Very Remote Australia", "Remote and Very Remote Australia", 
              "Northern Australia", "Regional Australia", "Bushfire declared areas",
              "Natural disaster declared areas"]
}
table_titles = pd.DataFrame(dictionnary_tablesTitles_gov_website)
data = pd.merge(cleaned_data, table_titles, on="Table number")

# Homogenize Job Types 
dictionnary_job_types = {
    "Job type": ["Tourism & Hospo", "Tourism & Hospo", "Tourism & Hospo", "Specified work", 
    "Natural disaster jobs", "Natural disaster jobs"],
    "Title": ["Remote and Very Remote Australia", "Remote and Very Remote Australia", 
              "Northern Australia", "Regional Australia", "Bushfire declared areas",
              "Natural disaster declared areas"]
}
table_job_types = pd.DataFrame(dictionnary_job_types)
data = pd.merge(data, table_job_types, on="Title")

data.to_csv('C:/Users/Proprietaire/Desktop/Code/Australia_map/Data_postcode_whv.csv', index=False)  
