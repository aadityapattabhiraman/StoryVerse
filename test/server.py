#!/usr/bin/env python3

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
import asyncio



app = FastAPI()

queue = asyncio.Queue()
MAX_REQUESTS_PER_MINUTE = 5
responses = {}

@app.on_event("startup")
async def startup_event():

    asyncio.create_task(queue_worker())


async def queue_worker():

    while True:

        request_id, input_time = await queue.get()

        if queue.empty():
            continue


        await queue_images(request_id, input_time)


async def queue_images(request_id, input_time):

    timestamps = []

    for _ in range(15):

        print(_)
        if len(timestamps) < 5:

            start_time = datetime.now().isoformat()
            print(start_time)
            timestamps.append(start_time)

        else:

            while True:

                if datetime.now().isoformat() > timestamps[0] + timedelta(minutes=1):
                    del timestamps[0]
                    break

        await handle_request()

    responses[request_id] = input_time


async def handle_request():

    await asyncio.sleep(1)


@app.post("/echo-time")
async def echo_time(request: Request):

    data = await request.json()
    input_time = data.get("time")

    request_id = str(datetime.now().timestamp()) + "-" + str(id(input_time))
    await queue.put((request_id, input_time))

    return JSONResponse(content={"message": "Request queued", "id": request_id})


@app.get("/get-response/{request_id}")
async def get_response(request_id: str):

    result = responses.get(request_id)

    if result:
        return {"received_time": result}

    else:
        return JSONResponse(status_code=202, content={"message": "Still processing..."})
