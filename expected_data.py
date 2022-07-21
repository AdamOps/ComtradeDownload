import os
import json
import pandas as pd
import numpy as np
from reporting_countries import reporting_country_list
from partner_countries import partner_country_list

## Working directory
username = os.environ.get("USERNAME")
cd = "C:/Users/" + username + "/OneDrive - SEO/Documenten/GEO Monitor/Data/"
os.chdir(cd)

with pd.ExcelFile("landen_HS_codes.xlsx") as tables:
    sheet2020 = pd.read_excel(tables, sheet_name="2020")
    sheet2019 = pd.read_excel(tables, sheet_name="2019")

cols = ["HS2017", "HS2012",	"HS2007", "HS2002", "HS1996", "HS1992"]

HS2017_2020 = sheet2020['HS2017']
HS2012_2020 = sheet2020['HS2012']
HS2007_2020 = sheet2020['HS2007']
HS2002_2020 = sheet2020['HS2002']
HS1996_2020 = sheet2020['HS1996']
HS1992_2020 = sheet2020['HS1992']

HS2017_2019 = sheet2019['HS2017']
HS2012_2019 = sheet2019['HS2012']
HS2007_2019 = sheet2019['HS2007']
HS2002_2019 = sheet2019['HS2002']
HS1996_2019 = sheet2019['HS1996']
HS1992_2019 = sheet2019['HS1992']

HS_2020 = HS2017_2020.append([HS2012_2020, HS2007_2020, HS2002_2020, HS1996_2020, HS1992_2020]).unique()
HS_2019 = HS2017_2019.append([HS2012_2019, HS2007_2019, HS2002_2019, HS1996_2019, HS1992_2019]).unique()

HS_2020 = [name.replace("\xa0", "") for name in HS_2020 if isinstance(name, str)]
HS_2019 = [name.replace("\xa0", "") for name in HS_2019 if isinstance(name, str)]

df_HS2020 = pd.DataFrame(pd.Series(HS_2020))
df_HS2020 = pd.concat([df_HS2020, pd.Series(np.ones(df_HS2020.shape[0]))], axis=1)
df_HS2020.columns = ["Country", "Available"]

df_HS2019 = pd.DataFrame(pd.Series(HS_2019))
df_HS2019 = pd.concat([df_HS2019, pd.Series(np.ones(df_HS2019.shape[0]))], axis=1)
df_HS2019.columns = ["Country", "Available"]

total_missing = pd.DataFrame(columns=['Folder', 'File', 'Size', 'Country', 'Partner Country', 'Size_flag', 'Available'])
files = [x for x in os.listdir(cd) if os.path.isfile(os.path.join(cd, x)) and x != "landen_HS_codes.xlsx"]
for file in files:
    df = pd.read_csv(file, sep=';', skiprows=1)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df.columns = ['Folder', 'File', 'Size', 'Country', 'Partner Country', 'Size_flag']
    if file.find("2020") > 0:
        df = pd.merge(df, df_HS2020, on="Country")
        df.to_csv("availability_test/availability_" + file, sep=';')
        total_missing = pd.concat([total_missing, df[df['Size_flag'] == True]])
    elif file.find("2019") > 0:
        df = pd.merge(df, df_HS2019, on="Country")
        df.to_csv("availability_test/availability_" + file, sep=';')
        total_missing = pd.concat([total_missing, df[df['Size_flag'] == True]])

total_missing = total_missing[total_missing['Country'] != total_missing['Partner Country']]
total_missing.to_csv("availability_test/availability_summary.csv", sep=';')
