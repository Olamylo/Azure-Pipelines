import requests
import json
import pandas as pd
from datetime import datetime
import time
import pyodbc
from sqlalchemy import create_engine
import os


def get_date(df,bulkid,date_added,location):
    df.insert(0,'bulk_id',bulkid)
    df.insert(1,'date_added',date_added)
    df.insert(2, 'location', location)
    return df

nigeria = os.environ.get("nigeria")
warsaw = os.environ.get("warsaw")
losangeles = os.environ.get("losangeles")

locations = [losangeles,warsaw,nigeria]
# locations = ["USA_los-angeles","POL_warsaw","NGA_lagos"]

count = 0
new_count = 0

list_df = pd.DataFrame()

for location in locations:
    print(location)

    url_api = f'https://api.midway.tomtom.com/ranking/liveHourly/{location}'

    usa_req = requests.get(url_api)

    usa_json = usa_req.json()

    # Do something with the json response to prove it works.
    print(usa_json)
    df = pd.json_normalize(usa_json['data'])

    df.UpdateTimeWeekAgo = pd.to_datetime(df.UpdateTimeWeekAgo, unit="ms")
    df.UpdateTime = pd.to_datetime(df.UpdateTime, unit="ms")


    bulkid = time.strftime('%Y%m%d%H%M')
    date_added = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    df = get_date(df,bulkid,date_added,location)
    list_df = pd.concat([list_df, df])

    new_count = count + 1

print(list_df)

