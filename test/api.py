import os
import base64
from openai import OpenAI



client = OpenAI(api_key=os.environ["OpenAI_Key"])

prompt = """
Create a image of a 18 year old girl overlooking a beach
"""

result = client.images.generate(
    model="gpt-image-1",
    prompt=prompt
)

image_base64 = result.data[0].b64_json
image_bytes = base64.b64decode(image_base64)

# Save the image to a file
with open("otter.png", "wb") as f:
    f.write(image_bytes)
