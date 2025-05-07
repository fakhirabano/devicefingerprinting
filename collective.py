import os
import pandas as pd

import numpy as np
import matplotlib.pyplot as plt

df_harvest1 = pd.read_csv('../june2018.csv', encoding = "ISO-8859-1")
df_harvest2 = pd.read_csv('../feb2019.csv', encoding = "ISO-8859-1")
df_harvest3 = pd.read_csv('../june2019.csv', encoding = "ISO-8859-1")


def prepareData(df_harvest):
    
    # All the top level domains coming from csv file
    df = pd.read_csv('./News-in-EU-PublicPrivate.csv')  
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
        country = row['Country']
        top_level_domain = row['TopLevelDomainLookUp']
        
        matching = df_harvest[df_harvest['script_url'].str.contains(top_level_domain) == True]
        
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
 
        country_bfps = []
        country_cfps = []
        country_cps = []
        d_f_p_array = []
        domain_names = []
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

    return {'country_list': country_list, 'dfp_values': d_f_p_values}


harvests = ['June 2018', 'February 2019', 'June 2019']
x_axis_len = len(harvests)

#result for harvest 1
result1=prepareData(df_harvest1)

#result for harvest 2
result2=prepareData(df_harvest2)

#result for harvest 3
result3=prepareData(df_harvest3)

all_countries1 = result1['country_list']
all_values1 = result1['dfp_values']
all_values2 = result2['dfp_values']
all_values3 = result3['dfp_values']
# print(len(all_values1))
harvests_dict = {}

for i in range(len(all_values1)):
    all_values = []
    all_values.append(all_values1[i]) 
    all_values.append(all_values2[i])
    all_values.append(all_values3[i])
    harvests_dict[all_countries1[i]] = all_values
# print (harvests_dict)
# print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
values_length = len(harvests)
h_length = values_length+1

df1=pd.DataFrame({'x': range(1, h_length), 'Austria':harvests_dict['Austria'], 'Belgium':harvests_dict['Belgium'],
                'Bulgaria':harvests_dict['Bulgaria'], 'Croatia':harvests_dict['Croatia'], 'Cyprus':harvests_dict['Cyprus'],
                'Czech Republic':harvests_dict['Czech Republic'], 'Denmark':harvests_dict['Denmark']})

df2=pd.DataFrame({'x': range(1, h_length), 'Estonia':harvests_dict['Estonia'],'Finland':harvests_dict['Finland'], 
                'France':harvests_dict['France'], 'Germany':harvests_dict['Germany'],'Greece':harvests_dict['Greece'], 
                'Hungary':harvests_dict['Hungary'], 'Ireland':harvests_dict['Ireland']})
                
df3=pd.DataFrame({'x': range(1, h_length), 'Italy':harvests_dict['Italy'], 'Latvia':harvests_dict['Latvia'], 
                'Lithuania':harvests_dict['Lithuania'], 'Luxembourg':harvests_dict['Luxembourg'], 'Malta':harvests_dict['Malta'], 
                'Netherlands':harvests_dict['Netherlands'], 'Poland':harvests_dict['Poland']})

df4=pd.DataFrame({'x': range(1, h_length), 'Portugal':harvests_dict['Portugal'], 'Romania':harvests_dict['Romania'],
                'Slovakia': harvests_dict['Slovakia'], 'Slovenia': harvests_dict['Slovenia'], 
                'Spain':harvests_dict['Spain'], 'Sweden':harvests_dict['Sweden'], 'UK':harvests_dict['UK']})

def create_plot(df):
    # style
    plt.style.use('seaborn-darkgrid')
    
    # create a color palette
    palette = plt.get_cmap('Set1')
    
    # multiple line plot
    num=0 
    for column in df.drop('x', axis=1):

        num+=1
        plt.plot(harvests, df[column], marker="o", color=palette(num), linewidth=2, alpha=0.9, label=column)
        
        # Add legend
        plt.legend(loc=1, ncol=2)
        
        # Add titles
        plt.title("A Commulative graph for all of three harvests ", loc='center', fontsize=12, fontweight=0, color='black')
        plt.xlabel("Data retrieved for countries in three point of times")
        plt.ylabel("Percentage levels of unique device fingerprinting from average of all the websites in each country")

    plt.show()

create_plot(df1)        # create plot for first set of  7 countries
create_plot(df2)        # create plot for second set of  7 countries
create_plot(df3)        # create plot for third set of  7 countries
create_plot(df4)        # create plot for last set of 7 countries

