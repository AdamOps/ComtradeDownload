import math
import time
import requests
import os
import pandas as pd

import functions
import comtrade_country_list as cclist

os.chdir("C:/Users/AdamKuczynski/OneDrive - SEO/Documenten/GEO Monitor/Data/")

# Just for convenience, storing the IDs of all countries in a list.
# Also storing all request URLs in a list, to then go through them one at a time.
# Felt like this was the most generalisable version.
countries = []
countryNames = []
urls = []
for country in cclist.country_list['results']:
    countries.append(str(country['id']))
    countryNames.append(str(country['text']))


# Fetching trade data for one partner country at a time.
# You could squeeze in more data per request, but it's unclear how much data each request actually covers
# E.g., NL->Afghanistan exports are <200 rows. NL->US is well over 1000.
# Ergo: Easier to go through it one country at a time.
request_param_list = []
for country in countries:
    new_request_params = functions.set_params(reporter=country,
                                              year="2021",
                                              frequency="A",
                                              classification="HS",
                                              partners="528",
                                              imports_or_exports="0",
                                              classification_code="AG6",
                                              return_format="csv",
                                              max_return="10000",
                                              goods_or_services="C",
                                              heading_style="H",
                                              imts_definition="2010")

    request_param_list.append(new_request_params)
    urls.append(functions.generate_link(new_request_params, False))

counter = 0
if len(urls) > 90:
    sleepTime = 36
else:
    sleepTime = 2
for link in urls:
    newData = requests.get(link)
    if request_param_list[counter]['rg'] == "1":
        filename = countryNames[counter] + "_exports_" + request_param_list[counter]['ps'] + ".csv"
    elif request_param_list[counter]['rg'] == "0":
        filename = countryNames[counter] + "_imports_" + request_param_list[counter]['ps'] + ".csv"
    else:
        print("Invalid parameters. Didn't specify whether it's imports or exports.")
        break
    counter += 1
    print("Retrieved file #", counter, " out of ", len(urls))
    hours = math.floor((len(urls)-counter)*sleepTime/3600)
    minutes = math.floor(((len(urls)-counter)*sleepTime - hours*3600)/60)
    print("Estimated time left: ", hours, "h", minutes)

    df_check = pd.DataFrame(newData)
    if df_check.loc[1,0] == "No data matches your query or your query is too complex. Request JSON or XML format for more information.,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,":
        continue
    open(filename, "wb").write(newData.content)

    # There's a limit to how many requests you can send per hour. With a guest account, it's 100 requests per hour.
    # With a licensed account, it's 1000.
    time.sleep(sleepTime)
