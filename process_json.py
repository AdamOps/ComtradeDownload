import json
import os
import pandas as pd
from os import listdir
from os.path import isfile, join

# cd = "C:/Users/AdamKuczynski/OneDrive - SEO/Documenten/GEO Monitor/Data/"
cd = "C:/Users/adamk/OneDrive - SEO/Documenten/GEO Monitor/Data/"
os.chdir(cd)
file_list = [f for f in listdir(cd) if isfile(join(cd, f))]

for json_file in file_list:
    with open(json_file) as file:
        data_file = json.load(file)
        data_DF = pd.DataFrame(data_file['dataset'])
        without_extension = json_file.rstrip(".json")
        export_name = cd + "csv_exports_2019/" + without_extension + ".csv"
        # print(export_name)
        data_DF.to_csv(export_name, sep=";")


