import os
import pandas as pd

import numpy as np
import matplotlib.pyplot as plt

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
  



for country_key, domains in countries.items():
    n_groups = len(domains)
    country_bfps = []
    country_cfps = []
    country_cps = []


    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.15
    opacity = 0.8

    domain_names = []
    # preparing bars data 
    for item in domains:
        for domain_name, domain in item.items():
            country_bfps.append(domain['b_f_p'])
            country_cfps.append(domain['c_f_p'])
            country_cps.append(domain['c_p'])
            domain_names.append(domain_name)
    

    rects1 = plt.bar(index, country_bfps, bar_width, alpha=opacity, color='b', label='Browser Fingerprinting')

    rects2 = plt.bar(index + bar_width, country_cfps, bar_width, alpha=opacity, color='g', label='Canvas Fingerprinting')

    rects3 = plt.bar(index + bar_width + bar_width, country_cps, bar_width, alpha=opacity, color='r', label='Cookie Printing')

    plt.xlabel('News Media Websites in '+country_key)
    plt.ylabel('Percentage')
    plt.title('Percentage by News Media Websites in '+country_key+ ' - June 2019 Data')
    plt.xticks(index + bar_width, domain_names)
    plt.xticks(rotation=80)
    
    plt.legend(loc=1)

    plt.tight_layout()
    plt.show()

   