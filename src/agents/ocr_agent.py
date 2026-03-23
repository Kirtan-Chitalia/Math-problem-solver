from src.agents.state import PipelineState
from src.vision.ocr import extract_text
from src.vision.llm_vision import extract_text_with_llm
from src.config import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


    
def ocr_agent(state: PipelineState) -> dict:
    image_path = state["image_path"]
    logger.info(f"OCR Agent processing: {image_path}")

    try:
        # ---- Step 1: Pix2Text ----
        result = extract_text(image_path)
        logger.info(f"Pix2Text raw result: {result}")

        # Safe extraction
        text = result.get("text", "")
        confidence = result.get("confidence", 0.0)
        source = result.get("source", "pix2text")

        # ---- Step 2: Confidence Check ----
        if confidence < settings.OCR_CONFIDENCE_THRESHOLD:
            logger.warning("Low OCR confidence. Falling back to LLM Vision.")

            llm_result = extract_text_with_llm(image_path)
            logger.info(f"LLM Vision raw result: {llm_result}")

            text = llm_result.get("text", text)
            confidence = llm_result.get("confidence", confidence)
            source = llm_result.get("source", "llm")

        else:
            logger.info("Using Pix2Text result")

        # ---- Step 3: Final Output ----
        return {
            "ocr_text": text,
            "ocr_confidence": confidence,
            "ocr_source": source
        }

    except Exception as e:
        logger.exception("OCR Agent failed")  # 🔥 shows full traceback

        return {
            "ocr_text": "",
            "ocr_confidence": 0.0,
            "ocr_source": "error",
            "error": str(e)
        }