from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from gpt import get_latex  # Импортируем функцию из вашего файла

app = FastAPI()

# Настройка логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/convert-to-latex")
async def convert_to_latex(image: UploadFile = File(...)):
    # Проверка типа файла
    if image.content_type is None or not image.content_type.startswith('image/'):
        logger.error("Uploaded file is not an image")
        raise HTTPException(400, detail="Uploaded file is not an image")

    try:
        # Чтение содержимого файла
        contents = await image.read()
        if not contents:
            logger.error("Empty file uploaded")
            raise HTTPException(400, detail="Uploaded image is empty")

        # Обработка изображения напрямую из памяти
        try:
            latex_code = get_latex(contents)
        except Exception as e:
            logger.error(f"Image processing error: {str(e)}", exc_info=True)
            raise HTTPException(
                500, detail=f"Image processing failed: {str(e)}")

        # Проверка результата
        if not latex_code or not latex_code.strip():
            logger.error("Empty LaTeX code generated")
            raise HTTPException(
                500, detail="Failed to generate valid LaTeX code")

        return {"latex_code": latex_code}

    except HTTPException as he:
        raise he

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            500, detail=f"Unexpected error occurred: {type(e).__name__}")
