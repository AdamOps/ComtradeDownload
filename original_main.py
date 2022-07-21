import math
import time
import requests
import os
import pandas as pd

import functions
from reporting_countries import reporting_country_list
from partner_countries import partner_country_list
import datetime

# Parameters
# Did Comtrade disconnect again?
comtrade_disconnected = False
disconnect_number = 0
all_countries = True
last_country = 0

## Working directory
username = os.environ.get("USERNAME")
cd = "C:/Users/" + username + "/OneDrive - SEO/Documenten/GEO Monitor/Data/"
os.chdir(cd)

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

if comtrade_disconnected:
    if all_countries:
        reporting_countries_id = reporting_countries_id[disconnect_number:]
        reporting_countries_names = reporting_countries_names[disconnect_number:]
    else:
        reporting_countries_id = reporting_countries_id[disconnect_number:last_country]
        reporting_countries_names = reporting_countries_names[disconnect_number:last_country]

for country in reporting_countries_id:
    new_request_params = functions.set_params(reporter=country,
                                              year="2019",
                                              frequency="A",
                                              classification="HS",
                                              partners="528",
                                              imports_or_exports="1",
                                              classification_code="AG6",
                                              return_format="json",
                                              max_return="10000",
                                              goods_or_services="C",
                                              heading_style="H",
                                              imts_definition="2010")

    request_param_list.append(new_request_params)
    urls.append(functions.generate_link(new_request_params, False))

if comtrade_disconnected:
    counter = disconnect_number
else:
    counter = 0

sleepTime = 40

for link in urls:
    print(link)
    newData = requests.get(link)
    if request_param_list[counter]['imports_or_exports'] == "2":
        filename = request_param_list[counter]['reporter'] + "_exports_to_" + request_param_list[counter]['partners'] + "_" + request_param_list[counter]['year']
    elif request_param_list[counter]['imports_or_exports'] == "1":
        filename = request_param_list[counter]['reporter'] + "_imports_from_" + request_param_list[counter]['partners'] + "_" + request_param_list[counter]['year']
    else:
        print("Invalid parameters. Didn't specify whether it's imports (1) or exports (2).")
        break

    if request_param_list[counter]['return_format'] == "csv":
        filename += ".csv"
    elif request_param_list[counter]['return_format'] == "json":
        filename += ".json"
    else:
        print("Invalid parameters. File-type not recognised. Set the return_format to either json or csv.")
        break
    counter += 1
    print("Retrieved file #", counter, " out of ", len(urls))
    print("Filename is: ", filename)
    print("Estimated time left: ", datetime.timedelta(0, (len(urls) - counter)*sleepTime))
    open(filename, "wb").write(newData.content)
    print("Retrieved file size: ", os.path.getsize(filename))

    time.sleep(sleepTime)
    if os.path.getsize(filename) < 700:
        newData = requests.get(link)
        if len(newData.headers['Content-Length']) < 700:
            print("Still no data. Very likely actually empty")
            time.sleep(sleepTime)
        else:
            print("Found new data after all. Thanks, Obama.")
            open(filename, "wb").write(newData.content)
            time.sleep(sleepTime)
