import os
import time
import base64
from openai import OpenAI


def pipeline():

    client = OpenAI(api_key=os.environ["OpenAI_Key"])

    start = time.time()

    prompt = """
Create a high quality hyper-realistic digital painting in the style of a traditional
oil painting. Recreate the exact composition, lighting, scene, and
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

    result = client.images.edit(
        model="gpt-image-1",
        image=[
            open("../data/evaluation/template.png", "rb"),
            open("../data/evaluation/user_1.jpg", "rb"),
            open("../data/evaluation/user_2.jpg", "rb")
        ],
        prompt=prompt
    )

    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    end = time.time()
    print(f"Time Taken: {end - start}")

    with open("../data/evaluation/multi_images.png", "wb") as f:
        f.write(image_bytes)

    print("../data/evaluation/multi_images.png", "COMPLETED")


if __name__ == "__main__":

    pipeline()
