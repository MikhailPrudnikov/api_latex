import base64
import openai
import os

API_KEY = os.getenv("API_GPT_KEY")

client = openai.OpenAI(api_key=API_KEY)


def encode_image(image_data: bytes) -> str:
    """Кодирует бинарные данные изображения в base64"""
    return base64.b64encode(image_data).decode('utf-8')


def get_latex(image_data) -> str:
    """
    Принимает бинарные данные изображения и возвращает LaTeX-код
    """
    base64_image = encode_image(image_data)

    response = client.responses.create(
        model="gpt-4o-mini-2024-07-18",
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Convert to LaTeX. Write only generated Latex code - no additional text is needed. Also do not add extra constructions - you only need to generate the formula and users themselves will decide how to put it into their files."},
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    },
                ],
            }
        ],
    )

    return (response.output_text)
