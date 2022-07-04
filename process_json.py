import json
import os
import pandas as pd
from os import listdir
from os.path import isfile, join, getsize
from datetime import datetime

# cd = "C:/Users/AdamKuczynski/OneDrive - SEO/Documenten/GEO Monitor/Data/"
cd = "C:/Users/adamk/OneDrive - SEO/Documenten/GEO Monitor/Data/imports_NL_from_country_2021_json/"
os.chdir(cd)
file_list = [f for f in listdir(cd) if isfile(join(cd, f))]

start = datetime.now()
counter = 0
for json_file in file_list:
    counter += 1
    if getsize(cd + json_file) > 500:
        with open(json_file) as file:
            data_file = json.load(file)
            data_DF = pd.DataFrame(data_file['dataset'])
            without_extension = json_file.rstrip(".json")
            export_name = cd + "../imports_NL_from_country_2021_csv/" + without_extension + ".csv"
            # print(export_name)
            data_DF.to_csv(export_name, sep=";")
            print("Processed ", counter, " out of ", len(file_list), " files.")


end = datetime.now()
delta = end-start
print("Done after ", delta, " seconds")
