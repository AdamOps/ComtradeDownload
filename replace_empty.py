import math
import time
import requests
import os
import pandas as pd

import functions
from reporting_countries import reporting_country_list
from partner_countries import partner_country_list
from os import listdir
from os.path import isfile, join, isdir
import datetime

## Working directory
username = os.environ.get("USERNAME")
cd = "C:/Users/" + username + "/OneDrive - SEO/Documenten/GEO Monitor/Data/"
os.chdir(cd)

## Parameters
continue_after_abortion = 0
errors_only = False
file_threshold = 700

##
urls = []
file_list = []

already_retrieved = [f for f in listdir(cd) if isfile(join(cd, f))]

if errors_only:
    file_threshold = 36

folder_list = [f for f in listdir(cd) if isdir(join(cd, f))]
for folder in folder_list:
    if folder.find("json") > 0 and folder == "imports_country_from_world_2020_json":
        files = [x for x in listdir(cd + folder) if isfile(join(cd + folder, x)) and os.path.getsize(cd + folder + "/" + x) <= file_threshold and x not in already_retrieved]
        for y in files:
            file_list.append(y)

for x in file_list:
    print(x)

request_param_list = []
years = []
reporter_loop_list = []
partner_loop_list = []
flow_loop_list = []

for file in file_list:
    splits = file.split("_")
    print(splits)
    if len(splits) != 3:
        reporter = splits[0]
        if splits[1] == "imports":
            flow = "1"
        else:
            flow = "2"
        if len(splits) == 4:
            partner = splits[2]
            year = splits[3].rstrip(".json")
        else:
            partner = splits[3]
            year = splits[4].rstrip(".json")
        reporter_loop_list.append(reporter)
        partner_loop_list.append(partner)
        years.append(year)
        flow_loop_list.append(flow)

for index in range(continue_after_abortion, len(reporter_loop_list)):
    new_request_params = functions.set_params(reporter=reporter_loop_list[index],
                                              year=years[index],
                                              frequency="A",
                                              classification="HS",
                                              partners=partner_loop_list[index],
                                              imports_or_exports=flow_loop_list[index],
                                              classification_code="AG6",
                                              return_format="json",
                                              max_return="10000",
                                              goods_or_services="C",
                                              heading_style="H",
                                              imts_definition="2010")

    request_param_list.append(new_request_params)
    urls.append(functions.generate_link(new_request_params, False))


counter = continue_after_abortion
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
    print("Retrieved file #", counter+1, " out of ", len(partner_loop_list))
    print("File name is: ", filename)
    print("Estimated time left: ", datetime.timedelta(0, (len(partner_loop_list) - counter)*sleepTime))
    open(filename, "wb").write(newData.content)
    print("Retrieved file size: ", os.path.getsize(filename))
    if os.path.getsize(filename) < 700:
        print("File seems empty. Double checking that there is actually no data to retrieve.")

    # There's a limit to how many requests you can send per hour. With a guest account, it's 100 requests per hour.
    # With a licensed account, it's 1000.
    time.sleep(sleepTime)
    if os.path.getsize(filename) < 700:
        newData = requests.get(link)
        if len(newData.headers['Content-Length']) < 700:
            print("Still no data. Very likely actually empty")
            time.sleep(sleepTime)
        else:
            print("Found new data after all. Thanks, Obama.")
            open(filename, "wb").write(newData.content)
    counter += 1
