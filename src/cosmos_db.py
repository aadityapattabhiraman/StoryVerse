import os
import asyncio
from azure.cosmos import CosmosClient, PartitionKey, exceptions



async def create_or_get_client():

    cosmos_url = os.environ["STORYVERSE_COSMOS_DB_URL"]
    cosmos_key = os.environ["STORYVERSE_COSMOS_DB_KEY"]
    client = await CosmosClient(cosmos_url, credential=cosmos_key)

    try:

        db_iter  = await client.list_databases()
        names = [db['id'] for db in db_iter]
        print("✅  Connected! Databases I can see:", names or "<none>")

    except exceptions.CosmosHttpResponseError as e:

        print(f"❌  Could not connect – status {e.status_code}")
        print("    Message:", e.message)

    return client


async def create_or_get_database(client):

    DATABASE_ID = "StoryVerse"

    try:

        database = await client.create_database_if_not_exists(id=DATABASE_ID)
        print(f"Database created or returned: {database.id}")
        return database

    except exceptions.CosmosHttpResponseError:

        print("Request to the Azure Cosmos database service failed.")


async def create_or_get_containers(client, database):

    containers = []

    try:

        partition_key_path = await PartitionKey(path="/categoryId")
        container = await database.create_container_if_not_exists(
            id="requests-info",
            partition_key=partition_key_path,
        )
        print(f"Container created or returned: {container.id}")
        containers.append(container)

        container = await database.create_container_if_not_exists(
            id="books-info",
            partition_key=partition_key_path,
        )
        print(f"Container created or returned: {container.id}")
        containers.append(container)

    except exceptions.CosmosHttpResponseError as e:

        print(f"Request to the Azure Cosmos database service failed:\n{e}")

    return containers


async def populate_container(container, items):

    for _ in items:

        inserted_item = await container.create_item(body=_)
        print("Inserted Story into StoryVerse.\n")
        print(f"Item id: {inserted_item['id']}\n")
        print(f"Number of images: {inserted_item['images']}\n")
        print(f"Blob Link: {inserted_item['blob-link']}")


async def query_items(container_obj, query_text):

    query_items_response = container_obj.query_items(
        query=query_text,
        enable_cross_partition_query=True
    )

    connection = container_obj.client_connection
    request_charge = connection.last_response_headers['x-ms-request-charge']
    items = [item async for item in query_items_response]
    print(f"Query returned {len(items)} items.")
    print(f"Operation consumed {request_charge} request units")

    return items


async def helper_function():

    client = await create_or_get_client()
    database = await create_or_get_database(client)
    containers = await create_or_get_containers(client, database)

    if len(containers) == 0:

        print("Database Error")
        exit()

    # Insert sample data
    sample_data = [
        {
            "id": "admin-trial",
            "images": 15,
            "blob-link": "https://idk.com/"
        },
        {
            "id": "admin-trial-1",
            "images": 16,
            "blob-link": "https://idk.com/"
        },
    ]

    await populate_container(containers[1], sample_data)

    



if __name__ == "__main__":

    asyncio.run(helper_function())
