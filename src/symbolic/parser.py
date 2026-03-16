import re
import sympy as sp
from src.utils import get_logger , ParserError

logger = get_logger(__name__)

def clean_ocr_text(raw: str) -> str:
    logger.info(f"Cleaning OCR text: {raw}")
    text = raw.strip()

    replacements = {

        # arithmetic
        "^": "**",
        "\\times": "*",
        "\\cdot": "*",
        "\\div": "/",

        # roots
        "\\sqrt": "sqrt",

        # calculus
        "\\int": "Integral",
        "\\sum": "Sum",
        "\\partial": "Derivative",

        # greek
        "\\alpha": "alpha",
        "\\beta": "beta",
        "\\gamma": "gamma",
        "\\delta": "delta",
        "\\epsilon": "epsilon",
        "\\varepsilon": "epsilon",
        "\\theta": "theta",
        "\\lambda": "lambda",
        "\\mu": "mu",
        "\\pi": "pi",
        "\\sigma": "sigma",
        "\\phi": "phi",
        "\\omega": "omega",

        # trig
        "\\sin": "sin",
        "\\cos": "cos",
        "\\tan": "tan",

        # logs
        "\\log": "log",
        "\\ln": "log",

        # remove latex wrappers
        "\\left": "",
        "\\right": "",

    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # convert \frac{a}{b} -> (a)/(b)
    text = re.sub(
        r"\\frac\s*\{([^}]*)\}\s*\{([^}]*)\}",
        r"(\1)/(\2)",
        text
    )

    # convert braces
    text = text.replace("{", "(").replace("}", ")")

    # √x -> sqrt(x)
    text = re.sub(r"√([a-zA-Z0-9]+)", r"sqrt(\1)", text)

    # |x| -> Abs(x)
    text = re.sub(r"\|([^|]+)\|", r"Abs(\1)", text)

    # remove commas
    text = text.replace(",", "")

    # collapse spaces
    text = re.sub(r"\s+", " ", text)

    # implicit multiplication 2x -> 2*x
    text = re.sub(r"(\d)([a-zA-Z])", r"\1*\2", text)

    # x(x+1) -> x*(x+1)
    text = re.sub(r"([a-zA-Z])\(", r"\1*(", text)

    logger.debug(f"Cleaned OCR text: {text}")
    return text


def parse_expression(raw: str):
    
    cleaned = clean_ocr_text(raw)

    try:

        if "=" in cleaned:

            parts = cleaned.split("=")

            lhs = parts[0]
            rhs = parts[-1]

            lhs_expr = sp.sympify(lhs)
            rhs_expr = sp.sympify(rhs)
            logger.info(f"Parsed as equation: {lhs_expr} = {rhs_expr}")
            return {
                "type": "equation",
                "lhs": lhs_expr,
                "rhs": rhs_expr,
                "raw": cleaned
            }

        else:

            expr = sp.sympify(cleaned)
            logger.info(f"Parsed as expression: {expr}")
            return {
                "type": "expression",
                "expr": expr,
                "raw": cleaned
            }

    except Exception as e:
        logger.error(f"Parse failed: {str(e)}")
        raise ParserError(f"Failed to parse: {cleaned}", details={"raw": raw, "cleaned": cleaned})