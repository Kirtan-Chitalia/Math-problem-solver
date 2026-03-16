from src.llm import LLMClient
from src.llm.prompts import PromptTemplates
from src.utils import get_logger, OCRError
from src.config import settings

logger = get_logger(__name__)


def extract_text_with_llm(image_path: str) -> dict:
    """
    Use a vision-capable LLM to extract math expressions from an image.

    Returns:
        {
            "text": "...",
            "confidence": 0.85,
            "source": "llm_vision"
        }
    """

    logger.info(f"Running LLM vision OCR for image: {image_path}")

    try:
        # 1. Create client
        client = LLMClient()

        # 2. Get prompt
        prompt = PromptTemplates.vision_ocr_prompt()

        # 3. Call LLM vision
        result = client.chat_with_image(
            prompt=prompt,
            image_path=image_path,
            model=settings.VISION_MODEL
        )

        result = result.strip()

        logger.info("Vision OCR successful")
        logger.debug(f"Vision OCR result preview: {result[:100]}")

        # 4. Return structured result
        return {
            "text": result,
            "confidence": 0.85,
            "source": "llm_vision"
        }

    except Exception as e:
        logger.error(f"Vision OCR failed: {str(e)}")
        raise OCRError(f"LLM vision OCR failed: {str(e)}")