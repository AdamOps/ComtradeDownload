import math
import time
import requests
import os
import pandas as pd

import functions
from reporting_countries import reporting_country_list
from partner_countries import partner_country_list


# Parameters
# Did Comtrade disconnect again?
comtrade_disconnected = False
disconnect_number = 0
all_countries = True
last_country = 0
double_check_empty_files = True

years = ['2019', '2020', '2021']

data_requests = {
    "request1": {
        "reporter": "all",
        "partner": "0",
        "flow": "2",
    },

    "request2": {
        "reporter": "all",
        "partner": "528",
        "flow": "1",
    },

    "request3": {
        "reporter": "all",
        "partner": "0",
        "flow": "1",
    },

    "request4": {
        "reporter": "528",
        "partner": "all",
        "flow": "1",
    },
}

os.chdir("C:/Users/AdamKuczynski/OneDrive - SEO/Documenten/GEO Monitor/Data/")
# os.chdir("C:/Users/adamk/OneDrive - SEO/Documenten/GEO Monitor/Data")

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

numTotalRequests = 0
numReporters = 0
numPartners = 0
numYears = len(years)
for request in data_requests:
    if data_requests[request]['reporter'] == "all":
        numReporters = len(reporting_countries_id)
    else:
        numReporters = 1
    if data_requests[request]['partner'] == "all":
        numPartners = len(partner_countries_id)
    else:
        numPartners = 1
    numTotalRequests += numYears * numReporters * numPartners

for request in data_requests:
    for year in years:
        if data_requests[request]['partner'] != "all":
            partner_loop_list = [data_requests[request]['partner']]
        else:
            partner_loop_list = partner_countries_id

        if data_requests[request]['reporter'] != 'all':
            reporter_loop_list = data_requests[request]['reporter']
        else:
            reporter_loop_list = reporting_countries_id

        for reporter_country in reporter_loop_list:
            for partner_country in partner_loop_list:
                new_request_params = functions.set_params(reporter=reporter_country,
                                                          year=year,
                                                          frequency="A",
                                                          classification="HS",
                                                          partners=partner_country,
                                                          imports_or_exports=data_requests[request]['flow'],
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
            print("Retrieved file #", counter, " out of ", numTotalRequests)
            print("Request: ", "reporter: ", request_param_list[counter]['reporter'], "; partner: ", request_param_list[counter]['partners'], "; year: ", year, "; flow: ", request_param_list[counter]['imports_or_exports'])
            open(filename, "wb").write(newData.content)

            # There's a limit to how many requests you can send per hour. With a guest account, it's 100 requests per hour.
            # With a licensed account, it's 1000.
            time.sleep(sleepTime)
            counter += 1
