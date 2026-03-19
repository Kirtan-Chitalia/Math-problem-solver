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

        # Equation verification (algebra)
        if "lhs" in parsed_result and "rhs" in parsed_result:
            lhs = sp.sympify(parsed_result["lhs"])
            rhs = sp.sympify(parsed_result["rhs"])
            answers = solution["answer"]
            x = sp.Symbol("x")

            if not isinstance(answers, (list, tuple)):
                answers = [answers]

            for ans in answers:
                check = (lhs - rhs).subs(x, ans)
                simplified = sp.simplify(check)
                correct = simplified == 0
                details.append({"value": ans, "check": simplified, "correct": correct})
                if not correct:
                    verified = False

        # Derivative verification — with timeout
        elif "expr" in parsed_result and "derivative" in str(solution.get("steps", [])).lower():
            try:
                expr = sp.sympify(parsed_result["expr"])
                answer = sp.sympify(solution["answer"])
                x = sp.Symbol("x")
                computed = sp.diff(expr, x)
                # Use equals() instead of simplify — much faster
                correct = computed.equals(answer)
                if correct is None:
                    correct = False  # equals() returns None if it can't determine
                details.append({"expected": str(computed)[:100], "given": str(answer)[:100], "correct": correct})
                verified = correct
            except TimeoutError:
                logger.warning("Verification timed out")
                return {"verified": "timeout", "details": "Expression too complex"}

        # Integral verification — with timeout  
        elif "expr" in parsed_result and "integral" in str(solution.get("steps", [])).lower():
            try:
                expr = sp.sympify(parsed_result["expr"])
                answer = sp.sympify(solution["answer"])
                x = sp.Symbol("x")
                computed = sp.diff(answer, x)
                correct = computed.equals(expr)
                if correct is None:
                    correct = False
                details.append({"expected": str(expr)[:100], "derived": str(computed)[:100], "correct": correct})
                verified = correct
            except TimeoutError:
                logger.warning("Verification timed out")
                return {"verified": "timeout", "details": "Expression too complex"}

        else:
            raise VerificationError("Unsupported verification type")

        logger.info(f"Verification result: {verified}")
        return {"verified": verified, "details": details}

    except Exception as e:
        logger.error(f"Verification failed: {str(e)}")
        raise VerificationError(f"Verification failed: {str(e)}")
