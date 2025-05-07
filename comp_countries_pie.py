import os
import pandas as pd

import numpy as np
import matplotlib.pyplot as plt
import statistics

# All the top level domains coming from csv file
df = pd.read_csv('./News-in-EU-PublicPrivate.csv')  

# df_harvest1 = pd.read_csv('../june2018.csv', encoding = "ISO-8859-1")
# df_harvest1 = pd.read_csv('../feb2019.csv', encoding = "ISO-8859-1")
df_harvest1 = pd.read_csv('../june2019.csv', encoding = "ISO-8859-1")

browser_finger_printing_variables = {
                  'window.navigator.userAgent': 20,'window.sessionStorage': 10,'window.navigator.platform':10, 
                  'window.navigator.language': 10,'window.localStorage': 10,'window.navigator.plugins': 20,
                  'window.navigator.doNotTrack': 10,'window.navigator.cookieEnabled': 10,
}

canvas_finger_printing_variables = {
                    'window.screen.colorDepth': 10 ,'window.screen.pixelDepth': 10, 'HTMLCanvasElement': 20, 'CanvasRenderingContext2D': 60,
}

cookie_finger_printing_variables = {'window.document.cookie': 100}

# countires dictionary
countries = {}
domains = []
for index, row in df.iterrows():
    
    # df.loc[df[script_url] == '' & df['symbol'] == '' ] can be for pattern matching
    # df['top_level_domain'] = ''       for defining a new column in the data set
    # df = df.drop(columns = ['top_level_domain'])       dropping the column - df = is imp
    country = row['Country']
    top_level_domain = row['TopLevelDomainLookUp']
    
    matching = df_harvest1[df_harvest1['script_url'].str.contains(top_level_domain) == True]
    
    # Browser finger printing matching and preparing data
    b_f_p_rows = {}
    b_f_p_percentage = 0
    for key, value in browser_finger_printing_variables.items():
        rows = matching[matching['symbol'].str.contains(key) == True]
        if rows.empty:
            b_f_p_rows[key]= 'No'     
        else:
            b_f_p_rows[key]= 'Yes'  
            b_f_p_percentage +=value
    
  
    # Canvas finger printing matching and preparing data
    c_f_p_rows = {}
    c_f_p_percentage = 0
    for key, value in canvas_finger_printing_variables.items():
        rows = matching[matching['symbol'].str.contains(key) == True]
        if rows.empty:
            c_f_p_rows[key]= 'No'     
        else:
            c_f_p_rows[key]= 'Yes'  
            c_f_p_percentage +=value

    # Cookies finger printing matching and preparing data
    c_p_rows = {}
    c_p_percentage = 0
    for  key, value in cookie_finger_printing_variables.items():
        rows = matching[matching['symbol'].str.contains(key) == True]
        if rows.empty:
            c_p_rows[key]= 'No'     
        else:
            c_p_rows[key]= 'Yes'
            c_p_percentage +=value 

    if country in countries:
        countries[country].append({top_level_domain: {'b_f_p': b_f_p_percentage, 'c_f_p': c_f_p_percentage, 'c_p': c_p_percentage } })
    else:
        countries[country] = []
        countries[country].append({top_level_domain: {'b_f_p': b_f_p_percentage, 'c_f_p': c_f_p_percentage, 'c_p': c_p_percentage } })


country_list = []
d_f_p_values = []

for country_key, domains in countries.items():
    # print(country_key)
#     n_groups = len(domains)
    country_bfps = []
    country_cfps = []
    country_cps = []
    d_f_p_array = []

#     # create plot
#     fig, ax = plt.subplots()
#     index = np.arange(n_groups)
#     bar_width = 0.15
#     opacity = 0.8


    domain_names = []
    d_f_p_array = []
    # preparing bars data 
    for item in domains:
        for domain_name, domain in item.items():
            country_bfps.append(domain['b_f_p'])
            country_cfps.append(domain['c_f_p'])
            country_cps.append(domain['c_p'])
            domain_names.append(domain_name)
    
            d_f_p_array.append(country_bfps)
            d_f_p_array.append(country_cfps)
            d_f_p_array.append(country_cps)

    # x = np.array(country_bfps, country_cfps, country_cps)
    country_list.append(country_key)
    d_f_p_values.append( round(np.mean(d_f_p_array), 2))


# Pie chart, where the slices will be ordered and plotted counter-clockwise:

# explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
labels = country_list
fig1, ax1 = plt.subplots()
patches, texts, autotexts = plt.pie(d_f_p_values, labels = country_list, autopct='%1.1f%%', pctdistance=0.85, startangle=90)

# plt.legend(patches, labels, title="Countries", loc = 2 , bbox_to_anchor=(1, 0, 0.5, 1))

plt.setp(autotexts, size=8, weight="bold")

centre_circle = plt.Circle((0,0),0.70,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.tight_layout()

plt.title('Comparison of EU countries capturing device fingerprinting - Data from June 2019')
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()
