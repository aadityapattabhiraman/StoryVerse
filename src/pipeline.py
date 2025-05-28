import os
import time
import base64
from datetime import datetime, timedelta
from openai import OpenAI



def get_images(data):

    images = []
    for image in os.listdir(data):

        if (image.endswith(".png")) or (image.endswith(".jpg")):
            images.append(image)

    return images


def pipeline():

    images = get_images("../data/Maya and the Little Flower/")[:6]
    mom = get_images("../data/pipeline/mom/")
    daughter = get_images("../data/pipeline/daughter/")
    client = OpenAI(api_key=os.environ["OpenAI_Key"])

    prompt = """
Create a hyper-realistic digital painting in the style of a traditional
oil painting in medium quality. Recreate the exact composition, lighting, scene, and
emotional atmosphere of the original reference image. Preserve every
element of the setting — including interior details, props, colors, and
light direction (e.g., golden sunlight, background furniture, windows,
wall art).

Maintain the original expressions, clothing, posture, body orientation,
and most importantly, the direction and focus of each person's eye
contact. Ensure all emotional cues and visual relationships between the
subjects remain intact.

Replace only the faces, hairstyles, and skin tones of the figures using
the provided portrait references. Integrate these new features
seamlessly, while keeping all other aspects — especially gesture,
expression, clothing, and positioning — completely unchanged.
Apply a warm, painterly brush texture and realistic lighting that
reflect traditional oil painting techniques. Ensure a natural,
emotionally coherent fusion of the swapped features into the scene,
preserving both realism and artistic depth.
    """

    timestamps = []

    for epoch in range(len(mom)):

        for _ in images:

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
                    open(f"../data/Maya and the Little Flower/{_}", "rb"),
                    open(f"../data/pipeline/mom/{mom[epoch]}", "rb"),
                    open(f"../data/pipeline/daughter/{daughter[epoch]}", "rb"),
                ],
                prompt=prompt
            )

            image_base64 = result.data[0].b64_json
            image_bytes = base64.b64decode(image_base64)

            # Save the image to a file
            if not os.path.exists(f"../data/results/{mom[epoch][:-4]}"):
                os.makedirs(f"../data/results/{mom[epoch][:-4]}/")
            with open(f"../data/results/{mom[epoch][:-4]}/{_}", "wb") as f:
                f.write(image_bytes)

            print(f"../data/results/{mom[epoch][:-4]}/{_}", "COMPLETED")

            end = time.time()
            print(f"Time Taken: {end - start}")


if __name__ == "__main__":

    pipeline()
