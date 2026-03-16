import cv2
from PIL import Image
from pix2text import Pix2Text
from pathlib import Path

from src.utils import get_logger, OCRError
from src.config import settings

logger = get_logger(__name__)

p2t = Pix2Text.from_config()


def preprocess_image(image_path: str):
    """Preprocess image for OCR."""

    logger.info(f"Preprocessing image: {image_path}")

    try:
        image_path = Path(image_path)

        if not image_path.exists():
            raise OCRError(f"Image not found: {image_path}")

        img = cv2.imread(str(image_path))

        if img is None:
            raise OCRError(f"Failed to read image: {image_path}")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        _, thresh = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

        return thresh

    except Exception as e:
        logger.error(f"Image preprocessing failed: {str(e)}")
        raise OCRError(f"OCR preprocessing failed: {str(e)}")


def extract_text(image_path: str) -> dict:
    """
    Extract math text from image using Pix2Text.

    Returns:
        {
            "text": "...",
            "confidence": 0.0–1.0,
            "source": "pix2text"
        }
    """

    logger.info(f"Starting OCR extraction for image: {image_path}")

    try:
        processed = preprocess_image(image_path)

        pil_img = Image.fromarray(processed)

        logger.debug("Running Pix2Text OCR")

        page = p2t(pil_img)

        texts = []

        for element in page.elements:
            if element.text:
                texts.append(element.text)

        result_text = " ".join(texts).strip()

        logger.debug(f"OCR raw output: {result_text}")

        confidence = _estimate_confidence(result_text)

        logger.info(f"OCR extraction complete | confidence={confidence:.2f}")

        return {
            "text": result_text,
            "confidence": confidence,
            "source": "pix2text"
        }

    except Exception as e:
        logger.error(f"OCR extraction failed: {str(e)}")
        raise OCRError(f"OCR text extraction failed: {str(e)}")


def _estimate_confidence(text: str) -> float:
    """Estimate OCR confidence based on output quality."""

    if not text or len(text.strip()) == 0:
        return 0.0

    score = 1.0

    if len(text.strip()) < 3:
        score -= 0.3

    # Garbage characters = bad OCR
    garbage_chars = sum(1 for c in text if c in "□■◊◦●")

    if garbage_chars > 0:
        score -= 0.3

    # Check if any math characters exist
    math_chars = set("0123456789+-*/=xyz()^{}\\")
    if not any(c in math_chars for c in text):
        score -= 0.4

    return max(0.0, min(1.0, score))