import sympy as sp
from src.utils import get_logger, SolverError

logger = get_logger(__name__)

def solve_algebra(lhs, rhs, variable="x") -> dict:
    """Solve an equation: lhs = rhs"""

    logger.info(f"Solving algebra equation: {lhs} = {rhs}")

    try:
        # 1. Create symbol
        x = sp.Symbol(variable)

        # 2. Create equation
        equation = sp.Eq(lhs, rhs)

        # 3. Solve equation
        solutions = sp.solve(equation, x)

        logger.debug(f"Solutions found: {solutions}")

        # 4. Return structured result
        return {
            "steps": [
                f"Created equation: {lhs} = {rhs}",
                f"Solved for {variable}"
            ],
            "answer": solutions
        }

    except Exception as e:
        logger.error(f"Algebra solver failed: {str(e)}")
        raise SolverError(f"Failed to solve algebra equation: {str(e)}")

def solve_calculus_derivative(expr, variable="x") -> dict:
    """Compute derivative of an expression"""

    logger.info(f"Solving calculus derivative for expression: {expr}")

    try:
        # 1. Create symbol
        x = sp.Symbol(variable)
        expr = sp.sympify(expr)
        # 2. Compute derivative
        result = sp.diff(expr, x)

        logger.debug(f"Derivative result: {result}")

        # 3. Return structured result
        return {
            "steps": [
                f"Computed derivative of {expr} with respect to {variable}"
            ],
            "answer": result
        }

    except Exception as e:
        logger.error(f"Calculus derivative solver failed: {str(e)}")
        raise SolverError(f"Failed to compute derivative: {str(e)}")

def solve_calculus_integral(expr, variable="x") -> dict:
    """Compute integral of an expression"""

    logger.info(f"Solving calculus integral for expression: {expr}")

    try:
        # 1. Create symbol
        x = sp.Symbol(variable)

        # Convert string expression to sympy expression if needed
        expr = sp.sympify(expr)

        # 2. Compute integral
        result = sp.integrate(expr, x)

        logger.debug(f"Integral result: {result}")

        # 3. Return structured result
        return {
            "steps": [
                f"Computed integral of {expr} with respect to {variable}"
            ],
            "answer": result
        }

    except Exception as e:
        logger.error(f"Calculus integral solver failed: {str(e)}")
        raise SolverError(f"Failed to compute integral: {str(e)}")

def solve(parsed_result: dict, problem_type: str) -> dict:
    """Dispatcher — routes to the right solver based on problem type"""

    logger.info(f"Solver dispatcher received problem type: {problem_type}")
    logger.debug(f"Parsed result: {parsed_result}")

    try:
        if problem_type == "algebra":
            return solve_algebra(
                parsed_result["lhs"],
                parsed_result["rhs"]
            )

        elif problem_type == "calculus_derivative":
            return solve_calculus_derivative(
                parsed_result["expr"]
            )

        elif problem_type == "calculus_integral":
            return solve_calculus_integral(
                parsed_result["expr"]
            )

        else:
            raise SolverError(f"Unsupported problem type: {problem_type}")

    except KeyError as e:
        logger.error(f"Missing required parsed field: {e}")
        raise SolverError(f"Missing required parsed field: {e}")

    except Exception as e:
        logger.error(f"Solver dispatcher failed: {str(e)}")
        raise SolverError(f"Solver dispatcher error: {str(e)}")
