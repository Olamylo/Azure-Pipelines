import requests
import json
import pandas as pd
from datetime import datetime
import time
import pyodbc
from sqlalchemy import create_engine
import os
from azure.storage.blob import BlobServiceClient

# Replace with your Azure Storage Account name and key
account_name = os.environ.get("account_name")
account_key = os.environ.get("account_key")

# Create the connection string
connection_string = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key}"
# connection_string = 'DefaultEndpointsProtocol=https;AccountName=account_name;AccountKey= account_key;EndpointSuffix=core.windows.net'

# Create the BlobServiceClient using the connection string
blob_service_client = BlobServiceClient.from_connection_string(connection_string)


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

    # new_count = count + 1
    # df.to_csv('./test_tomtom.csv',index = False, encoding= "utf-8")
# list_df.to_sql('STAGING_TOMTOM_TRAFFIC', con=engine, if_exists='replace', index=False)

print(list_df)

# Create a ContainerClient
container_name = "pythontest"
container = blob_service_client.get_container_client(container_name)

# Create a BlobClient
blob_name = "tomtom2_new.csv"
blob = container.get_blob_client(blob_name)

# If you want to be able to append data to the blob
blob.create_append_blob()

# If you want to create a new blob
# blob.upload_blob(list_df.to_csv().encode())

# Append data to blob
blob.append_block(list_df.to_csv().encode())




