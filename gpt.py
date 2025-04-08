import os
import base64
import openai


API_KEY = os.getenv("API_GPT_KEY")

client = openai.OpenAI(api_key=API_KEY)


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def fix(raw_latex: str) -> str:
    """
    Отправляет сырой LaTeX-код в ChatGPT и просит исправить ошибки компиляции.
    Возвращает откорректированный вариант.
    """
    developer_message = "You are helpful assistant whose task is to fix Latex code so that it compiles successfully. Write only fixed Latex code - no additional text is needed. Also do not add extra constructions - you only need to fix the given formula and users themselves will decide how to put it into their files"
    user_message = f"Fix this Latex code - {raw_latex}"
    try:
        response = client.chat.completions.create(
            model="o3-mini-2025-01-31",
            messages=[
                {
                    "role": "developer",
                    "content": developer_message
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            response_format={"type": "text"}
        )
        return response.choices[0].message.content
    except:
        return raw_latex


def get_latex(image_path) -> str:
    """
    Отправляет изображение в OpenAI и получает LaTeX-код.
    """
    base64_image = encode_image(image_path)

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
