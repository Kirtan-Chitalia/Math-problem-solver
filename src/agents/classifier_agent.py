from src.agents.state import PipelineState
from src.llm.client import LLMClient
from src.llm.prompts import PromptTemplates
from src.utils.logger import get_logger
from src.config import settings

logger = get_logger(__name__)

VALID_TYPES = {
    "algebra",
    "calculus_derivative",
    "calculus_integral",
    "linear_algebra",
    "differential_equation",
    "trigonometry",
    "arithmetic"
}

def classifier_agent(state: PipelineState) -> dict:
    """Uses LLM to classify the problem type."""

    ocr_text = state["ocr_text"]
    logger.info(f"Classifying problem: {ocr_text[:50]}...")

    try:
        # 1️⃣ Create LLM client
        client = LLMClient()

        # 2️⃣ Get prompts
        system_prompt = PromptTemplates.classifier_system_prompt()
        user_prompt = PromptTemplates.classifier_user_prompt(ocr_text)

        # 3️⃣ Call LLM
        response = client.chat(
            prompt=user_prompt,                # ✅ FIXED
            system_prompt=system_prompt,
            model=settings.CLASSIFIER_MODEL
        )

        # 4️⃣ Clean response
        problem_type = response.strip().lower()

        # 5️⃣ Validate
        if problem_type not in VALID_TYPES:
            logger.warning(f"Unknown classification: {problem_type}, defaulting to algebra")
            problem_type = "algebra"

        logger.info(f"Classifier result: {problem_type}")

        # 6️⃣ Return result
        return {
            "problem_type": problem_type
        }

    except Exception as e:
        logger.error(f"Classifier Agent failed: {str(e)}")

        # ✅ Graceful fallback
        return {
            "problem_type": "algebra",
            "error": f"Classifier failed: {str(e)}"
        }