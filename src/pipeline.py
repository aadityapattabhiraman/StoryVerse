import os
import base64
from openai import OpenAI



def pipeline():

    client = OpenAI(api_key=os.environ["OpenAI_Key"])
    prompt = """
Using the images provided create a hyper-realistic digital painting in traditional oil painting style. Recreate the exact composition, scene, lighting, and expressions of the original template image: a young girl and her grandmother sitting side by side at a wooden table indoors. In front of them are five small bowls filled with bright Holi powders. The room is softly lit with golden sunlight streaming through a window, featuring warm curtains, a bookshelf in the background, and a rainbow drawing on the wall. The girl’s face, hairstyle, and skin tone should be replaced with those from the provided photo of the young girl (braided hair with beads, smiling). Do not change her expression, posture, clothing, or body position—retain those exactly as in the template. The grandmother’s face, hairstyle, and skin tone should be swapped with those from the elderly woman in the second photo (white tied-back hair, red bindi, warm smile). Again, do not alter her expression, clothing, posture, or body orientation from the original template. Preserve the warm, painterly brush texture, the emotional ambiance, and the realistic lighting of the original oil painting.
    """
    result = client.images.edit(
        model="gpt-image-1",
        image=[
            open("../data/pipeline/template.png", "rb"),
            open("../data/pipeline/girl.jpg", "rb"),
            open("../data/pipeline/grandma.jpg", "rb"),
        ],
        prompt=prompt
    )

    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    # Save the image to a file
    with open("result.png", "wb") as f:
        f.write(image_bytes)


if __name__ == "__main__":

    pipeline()
