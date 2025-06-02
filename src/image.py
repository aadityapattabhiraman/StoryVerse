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
    template_images = get_images(story)
    print(template_images)
    situations = get_situation(f"{story}story.json")
    print(situations)
    descriptions = get_descritions(f"{story}descriptions.json")
    print(descriptions)


if __name__ == "__main__":

    pipeline()
