import os
import base64
from mimetypes import guess_type
from openai import AzureOpenAI
from typing import List


def data_url(image_path):

    mime_type, _ = guess_type(image_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'

    with open(image_path, "rb") as image_file:
        base64_encoded_data = base64.b64encode(image_file.read()).decode('utf-8')

    # return f"data:{mime_type};base64,{base64_encoded_data}"
    return base64_encoded_data


def get_images(directory: str) -> List[str]:

    images = []
    for image in os.listdir(directory):

        if (image.endswith(".png")) or (image.endswith(".jpg")):
            images.append(image)

    return images


def get_description(image):
    content = """
This task is for recreating character-neutral poses and forms using stylized or consent-based references. Facial details will be replaced in downstream processing. Descriptions are used solely to guide replication of general form, posture, and physical attributes without identity inference.
Prompt:
Describe the adult in the image in a way that can help replicate their general appearance for character-neutral image generation. Focus on the following attributes only:
Skin tone and complexion (e.g., light, medium brown, olive, etc.)
Hair color, length, and style
Body structure (e.g., height impression, slim/average/curvy build, posture)
General facial features (face shape, jawline, nose type, lips, cheekbones, eyebrow type, eye shape)
Do not describe facial expressions, identity-specific traits, cultural or religious markers, or accessories (e.g., glasses, jewelry, makeup, headwear, clothing details).
Begin with the phrase: “The man or woman or boy or girl image is...” and provide a clear, neutral, and reusable description.
    """

    response = client.chat.completions.create(
        model = deployment_name,
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": [
                {
                    "type": "text",
                    "text": content,
                },
                {
                    "type": "image_url",
                    "image": data_url(image)
                }
            ]}
        ],
        max_tokens=2000
    )

    print(response.choices[0].message.content)


if __name__ == "__main__":

    api_key = os.environ["AZURE_OPENAI_API_KEY"]
    api_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    deployment_name = "gpt-4o-mini"
    api_version = "2024-08-01-preview"

    client = AzureOpenAI(
        api_key=api_key,
        api_version=api_version,
    )

    images= get_images("../data/evaluation/men/")

    for _ in images:
        print(_)
        get_description("../data/evaluation/men/" + _)
