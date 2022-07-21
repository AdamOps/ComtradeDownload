import os
import json
import pandas as pd
from reporting_countries import reporting_country_list
from partner_countries import partner_country_list
import shutil

## Parameters
good_to_dumb = False
dumb_to_good = True

## Working directory
username = os.environ.get("USERNAME")
cd = "C:/Users/" + username + "/OneDrive - SEO/Documenten/GEO Monitor/Data/"
source = cd + "imports_country_from_world_2020_json/"
os.chdir(source)

file_list = [f for f in os.listdir(source) if os.path.isfile(os.path.join(source, f))]

if dumb_to_good:
    for file in file_list:
        reporter_name = file.split("_")[0]
        print("Looking for ", reporter_name)
        partner_name = "Netherlands"

        reporter_id = "-1"

        for reporter in reporting_country_list['results']:
            if reporter_name == reporter['text']:
                print("Found a match")
                reporter_id = reporter['id']
                break

        shutil.copy(file, str(reporter_id) + "_imports_from_0_2020.json")


if good_to_dumb:
    for file in file_list:
        reporter_name = "error"
        partner_name = "error"

        reporting_id = file.split("_")[0]
        partner_id = file.split("_")[3]
        for reporter in reporting_country_list['results']:
            if reporting_id == reporter['id']:
                reporter_name = reporter['text']

        shutil.copy(file, reporter_name + "_exports_2019.json")
