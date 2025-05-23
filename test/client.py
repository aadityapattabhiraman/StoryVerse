#!/usr/bin/env python3

import asyncio
import aiohttp
import datetime



URL = "http://127.0.0.1:8000"
TOTAL_REQUESTS = 20


async def send_and_wait(session, i):

    current_time = datetime.datetime.now().isoformat()
    payload = {"time": current_time}
    print(f"[{i+1}] Sending time: {current_time}")

    async with session.post(f"{URL}/echo-time", json=payload) as resp:

        data = await resp.json()
        request_id = data["id"]
        wait_time = data["expected_time"]
        print(wait_time)
        print(f"[{i+1}] Queued with ID: {request_id}")

    await asyncio.sleep(wait_time)

    while True:

        async with (
                session.get(f"{URL}/get-response/{request_id}")
        ) as resp:

            if resp.status == 200:

                result = await resp.json()
                response_time = datetime.datetime.now().isoformat()
                print(f"[{i+1}] Result: {result['received_time']}",
                      "(Response received at: {response_time})")

                print(f"[{i+1}] Request completed at: {response_time}")
                break


async def main():

    async with aiohttp.ClientSession() as session:

        tasks = [
            send_and_wait(session, i) for i in range(TOTAL_REQUESTS)
        ]
        await asyncio.gather(*tasks)



if __name__ == "__main__":

    asyncio.run(main())
