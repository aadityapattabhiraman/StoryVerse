#!/usr/bin/env python3

import asyncio

from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager



@asynccontextmanager
async def lifespan(app: FastAPI):

    task = asyncio.create_task(queue_worker())
    yield
    task.cancel()

    try:
        await task

    except asyncio.CancelledError:
        pass


app = FastAPI(lifespan=lifespan)
timestamps = []
MAX_REQUESTS_PER_MINUTE = 5
responses = {}
queue = asyncio.Queue()


async def queue_worker():

    while True:

        request_id, data = await queue.get()

        await queue_images(request_id, data)


async def queue_images(request_id, data):

    global timestamps
    num_images = 15

    for _ in range(num_images):

        if len(timestamps) < 5:

            start_time = datetime.now()
            timestamps.append(start_time)

        else:

            while True:

                if datetime.now() > timestamps[0] + timedelta(minutes=1):

                    del timestamps[0]
                    break

        await handle_requests(data)

    responses[request_id] = "DONE"


async def handle_requests(data):

    await asyncio.sleep(1)


@app.post("/get-request")
async def get_request(request: Request):

    request_data = await request.json()
    input_time = request_data.get("time")
    data = request_data.get("data")

    wait_time = (data["num_images"] / MAX_REQUESTS_PER_MINUTE) * 1
    request_id = str(datetime.now().timestamp()) + "-" + str(id(input_time))
    await queue.put((request_id, input_time))

    return JSONResponse(content={"message": "Request Queued", "id": request_id, "expected_time": wait_time})



@app.post("/post-request")
async def post_request(request_id: str):

    result = responses.get(request_id)

    if result:

        del responses[request_id]
        return {"Status": "Donw"}

    else:

        return JSONResponse(status_code=202, content={"message": "Still processing..."})
