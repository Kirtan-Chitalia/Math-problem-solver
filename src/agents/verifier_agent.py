from src.agents.state import PipelineState
from src.symbolic.verifier import verify
from src.utils import get_logger

logger = get_logger(__name__)

def verifier_agent(state: PipelineState) -> dict:
    logger.info("Starting verification agent")

    try:
        parsed = state.get("parsed", {})
        sympy_solution = state.get("sympy_solution", {})

        answer = sympy_solution.get("answer")

        # 🚨 NEW: sanity checks
        if not parsed:
            return {
                "verification": {
                    "verified": False,
                    "details": "Parsed expression missing"
                }
            }

        if answer is None:
            logger.warning("Skipping verification: No SymPy answer")
            return {
                "verification": {
                    "verified": "skipped",
                    "details": "No SymPy answer"
                }
            }

        # 🚨 NEW: handle empty / invalid answers
        if answer == "" or answer == []:
            return {
                "verification": {
                    "verified": False,
                    "details": "Empty answer from SymPy"
                }
            }

        logger.info(f"Answer to verify: {answer}")

        # 🔥 Safe verification
        try:
            result = verify(parsed, sympy_solution)
        except Exception as ve:
            logger.exception("Verification crashed")

            return {
                "verification": {
                    "verified": False,
                    "details": f"Verification error: {str(ve)}"
                }
            }

        return {"verification": result}

    except Exception as e:
        logger.exception("Verifier agent failed")

        return {
            "verification": {
                "verified": False,
                "details": f"Verifier failed: {str(e)}"
            },
            "error": str(e)
        }