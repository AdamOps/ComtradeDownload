import math
import time
import requests
import os
import pandas as pd

import functions
from reporting_countries import reporting_country_list
from partner_countries import partner_country_list


# os.chdir("C:/Users/AdamKuczynski/OneDrive - SEO/Documenten/GEO Monitor/Data/")
os.chdir("C:/Users/adamk/OneDrive - SEO/Documenten/GEO Monitor/Data")

# Just for convenience, storing the IDs of all countries in a list.
# Also storing all request URLs in a list, to then go through them one at a time.
# Felt like this was the most generalisable version.
reporting_countries_id = []
reporting_countries_names = []
partner_countries_id = []
partner_countries_names = []
urls = []
for country in reporting_country_list['results']:
    reporting_countries_id.append(str(country['id']))
    reporting_countries_names.append(str(country['text']))

for country in partner_country_list['results']:
    partner_countries_id.append(str(country['id']))
    partner_countries_names.append(str(country['text']))


# Fetching trade data for one partner country at a time.
# You could squeeze in more data per request, but it's unclear how much data each request actually covers
# E.g., NL->Afghanistan exports are <200 rows. NL->US is well over 1000.
# Ergo: Easier to go through it one country at a time.
request_param_list = []
for country in reporting_countries_id:
    new_request_params = functions.set_params(reporter=country,
                                              year="2019",
                                              frequency="A",
                                              classification="HS",
                                              partners="0",
                                              imports_or_exports="2",
                                              classification_code="AG6",
                                              return_format="json",
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
    print(link)
    newData = requests.get(link)
    if request_param_list[counter]['rg'] == "2":
        filename = reporting_countries_names[counter] + "_exports_" + request_param_list[counter]['ps']
    elif request_param_list[counter]['rg'] == "1":
        filename = reporting_countries_names[counter] + "_imports_" + request_param_list[counter]['ps']
    else:
        print("Invalid parameters. Didn't specify whether it's imports (1) or exports (2).")
        break

    if request_param_list[counter]['fmt'] == "csv":
        filename += ".csv"
    elif request_param_list[counter]['fmt'] == "json":
        filename += ".json"
    else:
        print("Invalid parameters. File-type not recognised. Set the return_format to either json or csv.")
        break
    counter += 1
    print("Retrieved file #", counter, " out of ", len(urls))
    hours = math.floor((len(urls)-counter)*sleepTime/3600)
    minutes = math.floor(((len(urls)-counter)*sleepTime - hours*3600)/60)
    print("Estimated time left: ", hours, "h", minutes)
    open(filename, "wb").write(newData.content)

    # There's a limit to how many requests you can send per hour. With a guest account, it's 100 requests per hour.
    # With a licensed account, it's 1000.
    time.sleep(sleepTime)
