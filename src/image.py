import os
import logging
import time
import base64
import json
from typing import List, Dict
from datetime import datetime, timedelta
from openai import OpenAI, BadRequestError


def get_images(directory: str) -> List[str]:

    images = []
    for image in os.listdir(directory):

        if (image.endswith(".png")) or (image.endswith(".jpg")):
            images.append(image)

    return images


def get_prompt(temp: str, kid: str, adult: str) -> str:

    prompt = f"""
    🎨 Scene & Emotion:
    Create a hyper-realistic digital painting based on the following scene description:
    {temp}
    Use the provided template image to guide the exact layout — including scene composition, pose, gestures, background elements, clothing, lighting, and overall emotional tone.

    👤 Character Identity Replacement (Descriptive Input):
    Replace the face, hairstyle, skin tone, and visible body type of both the child and the adult in the template image using the descriptions provided below. Ensure that the new characters are blended seamlessly into the original environment.

    🔹 Child Character Description:
    {kid}

    🔹 Adult Character Description:
    {adult}

    ✦ Preserve exactly:
    – Facial expression, eye direction, and head tilt
    – Body posture and gesture
    – Clothing and props
    – Scene lighting and painterly texture

    ✦ Do not change:
    – Composition, positioning, or atmosphere of the template image
    – The original emotion or visual storytelling

    🎨 Final Output:
    Blend the described characters into the scene with seamless realism and emotional consistency, matching the tone, detail, and storytelling of the original image. The result should appear as though the characters naturally belong in the environment.
    """

    return prompt


def get_situation(path: str) -> Dict:

    with open(path) as f:
        situations = json.load(f)

    return situations[0]


def get_descritions(path: str) -> Dict:

    with open(path) as f:
        descriptions = json.load(f)

    return descriptions


def pipeline():

    story = "../data/Maya and the Little Flower/"
    final = "../data/06-06/mult/"
    template_images = get_images(story)[4:6]
    situations = get_situation(f"{story}story.json")
    descriptions = get_descritions(f"{story}descriptions.json")[0]
    user_images = get_images("../data/evaluation/kids/")
    user_images_1 = get_images("../data/evaluation/adult/")
    kid, adult = get_descritions("../data/evaluation/desc.json")

    timestamps = []

    for i in range(2):

        if i == 0:
            situation = True

        else:
            situation = False

        j = 0
        for image in template_images:

            for _ in user_images[:1]:

                start = time.time()

                if len(timestamps) < 5:
                    timestamps.append(datetime.now())

                else:

                    while True:

                        if ((timestamps[0] + timedelta(minutes=1)) <
                                datetime.now()):

                            del timestamps[0]
                            timestamps.append(datetime.now())
                            break

                        time.sleep(1)

                if situation:
                    temp = situations.get(image[:-4])
                    prompt = get_prompt(temp, kid[f"{j + 1}"], adult[f"{j + 1}"])

                else:
                    temp = descriptions.get(image[:-4])
                    prompt = get_prompt(temp, kid[f"{j + 1}"], adult[f"{j + 1}"])

                while True:
                    try:

                        result = client.images.edit(
                            model="gpt-image-1",
                            image=[
                                open(f"{story}{image}", "rb"),
                                open(f"../data/evaluation/kids/{_}", "rb"),
                                open(f"../data/evaluation/adult/{user_images_1[j]}",
                                     "rb")
                            ],
                            prompt=prompt,
                        )

                        logging.debug(f"Template Image: {story}{image}")
                        logging.debug(f"Kid Image: kids/{_}")
                        logging.debug(f"Adult Image: adult/{user_images_1[j]}")
                        logging.debug(f"Prompt: {prompt}")

                        break

                    except BadRequestError as e:

                        logging.warning(f"{e}")
                        logging.warning(f"Template Image: {story}{image}")
                        logging.warning(f"Kid Image: kids/{_}")
                        logging.warning(f"Adult Image: adult/{user_images_1[j]}")
                        logging.warning(f"Prompt: {prompt}")

                        continue

                image_base64 = result.data[0].b64_json
                image_bytes = base64.b64decode(image_base64)

                end = time.time()
                print(f"Time Taken: {end - start}")

                if situation:
                    with open(f"{final}{_[:-4]}_{end - start}.png", "wb") as f:
                        f.write(image_bytes)

                else:
                    with open(f"{final}{_[:-4]}_{end - start}_des.png", "wb"
                              ) as f:
                        f.write(image_bytes)

                print(f"{final}{_[:-4]}_{end - start}.png COMPLETED")

                if j < 6:
                    j += 1

                else:
                    j = 0


if __name__ == "__main__":

    client = OpenAI(api_key=os.environ["OpenAI_Key"])
    logging.basicConfig(
        filename="logs.log",
        encoding="utf-8",
        filemode="a",
    )
    pipeline()
