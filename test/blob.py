#!/usr/bin/env python3

import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient



connect_str = os.getenv("STORYVERSE_BLOB_CONNECTION_STRING")

blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_name = "story-book-image-collection"
container_client = blob_service_client.get_container_client(container_name)
print("\nListing blobs...")

# List the blobs in the container
blob_list = container_client.list_blobs()
for blob in blob_list:
    print("\t" + blob.name)
