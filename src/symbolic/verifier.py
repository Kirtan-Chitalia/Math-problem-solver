import sympy as sp
from src.utils import get_logger, VerificationError

logger = get_logger(__name__)

def verify(parsed_result: dict, solution: dict) -> dict:
    """
    Verify a solution by substituting back into the original equation.
    """

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

            # Ensure answers is iterable
            if not isinstance(answers, (list, tuple)):
                answers = [answers]

            for ans in answers:
                check = (lhs - rhs).subs(x, ans)
                simplified = sp.simplify(check)

                correct = simplified == 0

                details.append({
                    "value": ans,
                    "check": simplified,
                    "correct": correct
                })

                if not correct:
                    verified = False

        # Derivative verification
        elif "expr" in parsed_result and "derivative" in str(solution.get("steps", [])).lower():
            expr = sp.sympify(parsed_result["expr"])
            answer = sp.sympify(solution["answer"])
            x = sp.Symbol("x")
            computed = sp.diff(expr, x)
            correct = sp.simplify(computed - answer) == 0
            details.append({"expected": computed, "given": answer, "correct": correct})
            verified = correct

        # Integral verification
        elif "expr" in parsed_result and "integral" in str(solution.get("steps", [])).lower():
            expr = sp.sympify(parsed_result["expr"])
            answer = sp.sympify(solution["answer"])
            x = sp.Symbol("x")
            computed = sp.diff(answer, x)  # differentiate the answer
            correct = sp.simplify(computed - expr) == 0
            details.append({"expected": expr, "derived_from_answer": computed, "correct": correct})
            verified = correct

        else:
            raise VerificationError("Unsupported verification type")

        logger.info(f"Verification result: {verified}")

        return {
            "verified": verified,
            "details": details
        }

    except Exception as e:
        logger.error(f"Verification failed: {str(e)}")
        raise VerificationError(f"Verification failed: {str(e)}")