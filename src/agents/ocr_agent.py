from src.agents.state import PipelineState
from src.vision.ocr import extract_text
from src.vision.llm_vision import extract_text_with_llm
from src.config import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


    
def ocr_agent(state: PipelineState) -> dict:
    """
    OCR Agent — extracts math text from an image.
    Tries Pix2Text first, falls back to LLM Vision if confidence is low.
    """
    image_path = state["image_path"]
    logger.info(f"OCR Agent processing: {image_path}")
        
    try:
        # 1. Try Pix2Text first 
        result = extract_text(image_path)
        logger.info(f"Pix2Text result: {result}")
        # 2. Check confidence against threshold
        if result["confidence"] >= settings.OCR_CONFIDENCE_THRESHOLD:
            logger.info("OCR confidence is sufficient. Using Pix2Text result.")

        else:
            logger.warning("Low OCR confidence. Falling back to LLM Vision.")
            result = extract_text_with_llm(image_path)
            logger.info(f"LLM Vision result: {result}")

        # 3. Return the state updates
        return {
            "ocr_text": result["text"],
            "ocr_confidence": result["confidence"],
            "ocr_source": result["source"]
        }
    except Exception as e:
        logger.error(f"OCR Agent failed: {str(e)}")

        return {
            "ocr_text": "",
            "ocr_confidence": 0.0,
            "ocr_source": "error",
            "error": f"OCR failed: {str(e)}"
        }

    