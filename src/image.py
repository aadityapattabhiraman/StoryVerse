import os
import time
import base64
import json
from typing import List
from datetime import datetime, timedelta
from openai import OpenAI


def get_images(directory: str) -> List[str]:

    images = []
    for image in os.listdir(directory):

        if (image.endswith(".png")) or (image.endswith(".jpg")):
            images.append(image)

    return images


def get_prompt(path: str) -> str:

    print(path)
    prompt = """"""

    return prompt


def get_situation(path: str) -> List:

    with open(path) as f:
        situations = json.load(f)

    return situations


def get_descritions(path: str) -> List:

    with open(path) as f:
        descriptions = json.load(f)

    return descriptions


def pipeline():

    story = "../data/Maya and the Little Flower/"
    final = "../data/04-06/"
    template_images = get_images(story)
    print(template_images)
    situations = get_situation(f"{story}story.json")
    print(situations)
    descriptions = get_descritions(f"{story}descriptions.json")
    print(descriptions)
    user_images = get_images("../data/evaluation/kids/")

    timestamps = []

    for image in template_images:

        for _ in user_images:

            start = time.time()

            if len(timestamps) < 5:
                timestamps.append(datetime.now())

            else:

                while True:

                    if (timestamps[0] + timedelta(minutes=1)) < datetime.now():

                        del timestamps[0]
                        timestamps.append(datetime.now())
                        break

                    time.sleep(1)

            result = client.images.edit(
                model="gpt-image-1",
                image=[
                    open(f"{story}{image}", "rb"),
                    open(f"{story}{_}", "rb"),
                ],
                prompt=None,
            )

            image_base64 = result.data[0].b64_json
            image_bytes = base64.b64decode(image_base64)

            end = time.time()
            print(f"Time Taken: {end - start}")

            with open(f"{final}{_:-4}_{end - start}.png", "wb") as f:
                f.write(image_bytes)

            print(f"{final}{_:-4}_{end - start}.png COMPLETED")


if __name__ == "__main__":

    client = OpenAI(api_key=os.environ["OpenAI_Key"])
    pipeline()
