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

os.chdir("C:/Users/AdamKuczynski/OneDrive - SEO/Documenten/GEO Monitor/Data/")
# os.chdir("C:/Users/adamk/OneDrive - SEO/Documenten/GEO Monitor/Data")

reporting_countries_id = []
reporting_countries_names = []
partner_countries_id = []
partner_countries_names = []
years = []
empty_files = []

urls = []

file_list = []

cd = "C:/Users/AdamKuczynski/OneDrive - SEO/Documenten/GEO Monitor/Data/"
folder_list = [f for f in listdir(cd) if isdir(join(cd, f))]
for folder in folder_list:
    if folder.find("json") > 0:
        files = [x for x in listdir(cd + folder) if isfile(join(cd + folder, x)) and os.path.getsize(cd + folder + "/" + x) < 700 and os.path.getmtime(cd + folder + "/" + x) > 1]
        for y in files:
            file_list.append(y)
# for file in file_list:
    # print(file)

# print(len(file_list))

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

for index in range(0, len(reporter_loop_list)):
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
    print("Retrieved file #", counter, " out of ", len(partner_loop_list))
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
            empty_files.append(filename)
            time.sleep(sleepTime)
        else:
            print("Found new data after all. Thanks, Obama.")
            open(filename, "wb").write(newData.content)
    counter += 1

for file in empty_files:
    open("empty_files.txt", "wb").write(file + "\n")
