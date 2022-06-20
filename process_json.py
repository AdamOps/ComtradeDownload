import json
import os
import pandas as pd
from os import listdir
from os.path import isfile, join

cd = "C:/Users/AdamKuczynski/OneDrive - SEO/Documenten/GEO Monitor/Data/"
os.chdir(cd)
source_data = cd + "imports_country_from_NL_2019_json/"
file_list = [f for f in listdir(source_data) if isfile(join(source_data, f))]

for json_file in file_list:
    if os.path.getsize(source_data + json_file) > 500:
        with open(source_data + json_file) as file:
            data_file = json.load(file)
            data_DF = pd.DataFrame(data_file['dataset'])
            without_extension = json_file.rstrip(".json")
            export_name = cd + "imports_country_from_NL_2019_csv/" + without_extension + ".csv"
            # print(export_name)
            data_DF.to_csv(export_name, sep=";")


