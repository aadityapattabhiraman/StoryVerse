#!/usr/bin/env python3

import os
from azure.cosmos import CosmosClient, exceptions



cosmos_url = os.environ["STORYVERSE_COSMOS_DB_URL"]
cosmos_key = os.environ["STORYVERSE_COSMOS_DB_KEY"]
client = CosmosClient(cosmos_url, credential=cosmos_key)

try:

    db_iter  = client.list_databases()
    names = [db['id'] for db in db_iter]
    print("✅  Connected! Databases I can see:", names or "<none>")

except exceptions.CosmosHttpResponseError as e:

    print(f"❌  Could not connect – status {e.status_code}")
    print("    Message:", e.message)
