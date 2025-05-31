import os
import time
import base64
from datetime import datetime, timedelta
from openai import OpenAI



def get_images(data):

    images = []
    for image in os.listdir(data):

        if (image.endswith(".png")) or (image.endswith(".jpg")) or (image.endswith(".avif")):
            images.append(image)

    return images


def pipeline():

    images = get_images("../data/Maya and the Little Flower/")[0]
    kids = get_images("../data/evaluation/kids/")
    client = OpenAI(api_key=os.environ["OpenAI_Key"])

    situation = "Maya ran outside with a small plastic cover in her hand. As she reached the flower, she slipped in the mud and fell to her knees. She scrambled up, soaked and muddy, determined to protect Lila."

    prompt = f"""
Create a high-quality hyper-realistic digital painting in the style of a traditional oil painting. Reproduce the original composition, lighting, scene, and emotional atmosphere exactly as in the reference image, including all interior details, props, colors, and light direction.
 
Preserve every aspect of the setting and figures — including expressions, clothing, posture, body orientation, and eye contact direction. Replace only the faces, hairstyles, and skin tones of the figures using the provided portrait references, while ensuring that the facial features match those in the template image exactly.
 
Integrate the new features seamlessly, maintaining realistic lighting, emotional coherence, and a painterly brush texture consistent with traditional oil painting techniques. Ensure the fusion of the swapped features feels natural and artistically authentic.
Make sure the image that you generate is of equal dimensions.
This is the context:
    {situation}
    """

    timestamps = []

    for epoch in range(1):

        for _ in kids:

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
                    open(f"../data/Maya and the Little Flower/{images}", "rb"),
                    open(f"../data/evaluation/kids/{_}", "rb"),
                ],
                prompt=prompt
            )

            image_base64 = result.data[0].b64_json
            image_bytes = base64.b64decode(image_base64)

            end = time.time()
            print(f"Time Taken: {end - start}")

            with open(f"../data/evaluation/result/{_[:-4]}_{end-start}_3prompt.png", "wb") as f:
                f.write(image_bytes)

            print(f"../data/evaluation/result/{_[:-4]}_{end-start}_3prompt.png", "COMPLETED")



if __name__ == "__main__":

    pipeline()
