import os
import json
import pandas as pd
from reporting_countries import reporting_country_list
from partner_countries import partner_country_list

## Working directory
username = os.environ.get("USERNAME")
cd = "C:/Users/" + username + "/OneDrive - SEO/Documenten/GEO Monitor/Data/"
os.chdir(cd)

folder_list = [f for f in os.listdir(cd) if os.path.isdir(os.path.join(cd, f))]
for folder in folder_list:
    if folder.find("json") > 0 and folder.find("back") < 0:
        name_list = []
        partner_list = []
        file_list = []
        size_list = []
        curr_folder = []
        size_flag = []

        files = [x for x in os.listdir(cd + folder) if os.path.isfile(os.path.join(cd + folder, x))]
        for file in files:
            print(file)
            reporter_name = "error"
            partner_name = "error"
            reporting_id = file.split("_")[0]
            partner_id = file.split("_")[3]
            for reporter in reporting_country_list['results']:
                if reporting_id == reporter['id']:
                    reporter_name = reporter['text']
                    break
            for partner in partner_country_list['results']:
                if partner_id == partner['id']:
                    partner_name = partner['text']
                    break

            name_list.append(reporter_name)
            partner_list.append(partner_name)
            curr_folder.append(folder)
            file_list.append(file)
            size_list.append(os.path.getsize(cd + folder + "/" + file))
            size_flag.append(os.path.getsize(cd + folder + "/" + file) < 700)

        size_overview = pd.DataFrame(curr_folder)
        size_overview = pd.concat([size_overview, pd.Series(file_list), pd.Series(size_list), pd.Series(name_list), pd.Series(partner_list), pd.Series(size_flag)], axis=1)
        size_overview.columns = ['Folder', 'File', 'Size', 'Country', 'Partner Country', 'Size_flag']

        output_file = open(folder + "_got_data.csv", "w")
        output_file.truncate()
        output_file.write(f"sep=;\n")
        output_file.close()
        size_overview.to_csv(folder + "_got_data.csv", mode='a', header=True, index=True, sep=';')
