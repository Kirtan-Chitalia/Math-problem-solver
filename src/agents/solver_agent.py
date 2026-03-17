from src.agents.state import PipelineState
from src.llm.client import LLMClient
from src.llm.prompts import PromptTemplates
from src.symbolic.parser import parse_expression
from src.symbolic.solver import solve
from src.config import settings
from src.utils import get_logger

logger = get_logger(__name__)

def solver_agent(state: PipelineState) -> dict:
    """Hybrid solver — LLM for steps, SymPy for verification."""

    ocr_text = state["ocr_text"]
    problem_type = state["problem_type"]
    logger.info(f"Solving [{problem_type}]: {ocr_text[:50]}...")

    try:
        # 1. LLM solution (step-by-step for the user)
        client = LLMClient()

        system = PromptTemplates.solver_system_prompt(problem_type)
        user = PromptTemplates.solver_user_prompt(ocr_text)

        llm_response = client.chat(
            prompt=user,
            system_prompt=system,
            model=settings.SOLVER_MODEL
        )

        # 2. SymPy solution (for verification)
        try:
            parsed = parse_expression(ocr_text)
            sympy_result = solve(parsed, problem_type)

        except Exception as sympy_error:
            logger.warning(f"SymPy failed: {str(sympy_error)}")

            parsed = {}
            sympy_result = {
                "steps": [],
                "answer": None,
                "error": str(sympy_error)
            }

        # 3. Return both:
        return {
               "llm_solution": llm_response,
               "sympy_solution": sympy_result,
               "parsed": parsed
           }

    except Exception as e:
        logger.error(f"Solver agent failed: {str(e)}")

        return {
            "llm_solution": "",
            "sympy_solution": {},
            "parsed": {},
            "error": f"Solver failed: {str(e)}"
        }