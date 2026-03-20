import sympy as sp
from src.utils import get_logger, VerificationError
import signal
import functools

logger = get_logger(__name__)

VERIFY_TIMEOUT = 10  # seconds

def verify(parsed_result: dict, solution: dict) -> dict:
    """Verify a solution by substituting back into the original equation."""
    logger.info("Starting verification process")

    try:
        details = []
        verified = True
        # Decide verification type based on parsed_result and solver steps
        steps_str = str(solution.get("steps", [])).lower()

        # --- Calculus derivative verification ---
        if "derivative" in steps_str:
            try:
                # expression may be under 'expr' or 'rhs' (for y = f(x) style)
                expr_src = parsed_result.get("expr") or parsed_result.get("rhs")
                expr = sp.sympify(expr_src)
                answer = sp.sympify(solution["answer"])
                x = sp.Symbol("x")
                computed = sp.diff(expr, x)
                correct = computed.equals(answer)
                if correct is None:
                    correct = False
                details.append({"expected": str(computed)[:200], "given": str(answer)[:200], "correct": correct})
                verified = correct
            except TimeoutError:
                logger.warning("Verification timed out")
                return {"verified": "timeout", "details": "Expression too complex"}

        # --- Calculus integral verification ---
        elif "integral" in steps_str:
            try:
                expr_src = parsed_result.get("expr") or parsed_result.get("rhs")
                expr = sp.sympify(expr_src)
                answer = sp.sympify(solution["answer"])
                x = sp.Symbol("x")
                computed = sp.diff(answer, x)
                correct = computed.equals(expr)
                if correct is None:
                    correct = False
                details.append({"expected": str(expr)[:200], "derived": str(computed)[:200], "correct": correct})
                verified = correct
            except TimeoutError:
                logger.warning("Verification timed out")
                return {"verified": "timeout", "details": "Expression too complex"}

        # --- Algebra / direct equation verification ---
        elif "lhs" in parsed_result and "rhs" in parsed_result:
            lhs = sp.sympify(parsed_result["lhs"])
            rhs = sp.sympify(parsed_result["rhs"])
            answers = solution.get("answer")
            x = sp.Symbol("x")

            if not isinstance(answers, (list, tuple)):
                answers = [answers]

            for ans in answers:
                # Only substitute when the answer is a concrete value for the variable
                try:
                    check = (lhs - rhs).subs(x, ans)
                    simplified = sp.simplify(check)
                    correct = simplified == 0
                except Exception:
                    simplified = None
                    correct = False

                details.append({"value": ans, "check": simplified, "correct": correct})
                if not correct:
                    verified = False

        else:
            raise VerificationError("Unsupported verification type")

        logger.info(f"Verification result: {verified}")
        return {"verified": verified, "details": details}

    except Exception as e:
        logger.error(f"Verification failed: {str(e)}")
        raise VerificationError(f"Verification failed: {str(e)}")
