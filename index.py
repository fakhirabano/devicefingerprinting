import os
import pandas as pd
# import jinja2


# All the top level domains coming from csv file
df = pd.read_csv('./News-in-EU-PublicPrivate.csv')  
# df = pd.read_csv('./topdom.csv')  



# df_harvest1 = pd.read_csv('../2019-06-14-optimized.csv', skiprows = lambda x,y: mylogic(x,y) , encoding = "ISO-8859-1")
df_harvest1 = pd.read_csv('../feb2019.csv', encoding = "ISO-8859-1")

browser_finger_printing_variables = [
                    'window.navigator.userAgent', 'window.sessionStorage', 'window.navigator.platform', 'window.navigator.language',
                    'window.localStorage', 'window.navigator.plugins','window.navigator.doNotTrack', 'window.navigator.cookieEnabled',
                ]
canvas_finger_printing_variables = [
                    'window.screen.colorDepth','window.screen.pixelDepth', 'HTMLCanvasElement', 'CanvasRenderingContext2D',
                ]

cookie_finger_printing_variables = ['window.document.cookie']


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

    for key in browser_finger_printing_variables:
        print(key)
        # rows = matching[matching['symbol'].str.contains(key) == True]
        # # b_f_p_rows[key] = rows['value']       
        # if rows.empty:
        #     b_f_p_rows[key]= 'No'     
        # else:
        #     b_f_p_rows[key]= 'Yes' 


    # Canvas finger printing matching and preparing data
    # c_f_p_rows = {}

    # for key in canvas_finger_printing_variables:
        # rows = matching[matching['symbol'].str.contains(key) == True]
        # # c_f_p_rows[key] = rows['value']       
        # if rows.empty:
        #     c_f_p_rows[key]= 'No'     
        # else:
        #     c_f_p_rows[key]= 'Yes' 

    # Cookies finger printing matching and preparing data
    # c_p_rows = {}

    # for key in cookie_finger_printing_variables:
        # rows = matching[matching['symbol'].str.contains(key) == True]
        # # c_p_rows[key] = rows['value']       
        # if rows.empty:
        #     c_p_rows[key]= 'No'     
        # else:
        #     c_p_rows[key]= 'Yes' 

    # if country in countries:
    #     countries[country].append({top_level_domain: {'b_f_p': b_f_p_rows, 'c_f_p': c_f_p_rows, 'c_p_rows': c_p_rows } })
    # else:
    #     countries[country] = []
    #     countries[country].append({top_level_domain: {'b_f_p': b_f_p_rows, 'c_f_p': c_f_p_rows, 'c_p_rows': c_p_rows } })
  
 


# print(countries)



# templateLoader = jinja2.FileSystemLoader(searchpath="./")
# templateEnv = jinja2.Environment(loader=templateLoader)
# TEMPLATE_FILE = "pdf_interest_report.html"
# template = templateEnv.get_template(TEMPLATE_FILE)


# outputText = template.render('pdf_interest_report.html')
# html_file = open(str(int(d['interest_rate'] * 100)) + '.html', 'w')
# html_file.write(outputText)
# html_file.close()