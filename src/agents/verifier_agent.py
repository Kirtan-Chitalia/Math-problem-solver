from src.agents.state import PipelineState
from src.symbolic.verifier import verify
from src.utils import get_logger

logger = get_logger(__name__)

def verifier_agent(state: PipelineState) -> dict:
    """Verifier Agent — checks correctness of SymPy solution."""

    logger.info("Starting verification agent")

    try:
        # 1️⃣ Get required data
        parsed = state.get("parsed", {})
        sympy_solution = state.get("sympy_solution", {})

        answer = sympy_solution.get("answer")

        # 2️⃣ If SymPy has a valid answer → verify
        if answer is not None:
            logger.info("Verifying SymPy solution")

            result = verify(parsed, sympy_solution)

            return {
                "verification": result
            }

        # 3️⃣ If SymPy failed → skip verification
        else:
            logger.warning("Skipping verification: No SymPy answer")

            return {
                "verification": {
                    "verified": "skipped",
                    "details": "No SymPy answer"
                }
            }

    except Exception as e:
        logger.error(f"Verifier agent failed: {str(e)}")

        return {
            "verification": {
                "verified": False,
                "details": f"Verification failed: {str(e)}"
            },
            "error": f"Verifier failed: {str(e)}"
        }