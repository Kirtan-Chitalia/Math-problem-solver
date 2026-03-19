import re
import sympy as sp
from src.utils import get_logger, ParserError
from latex2sympy2 import latex2sympy

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


def _strip_latex_delimiters(raw: str) -> str:
    """Strip $$, $, and \\[ \\] LaTeX delimiters."""
    text = raw.strip()
    # Remove $$ ... $$ or $ ... $
    if text.startswith("$$") and text.endswith("$$"):
        text = text[2:-2].strip()
    elif text.startswith("$") and text.endswith("$"):
        text = text[1:-1].strip()
    # Remove \[ ... \]
    if text.startswith("\\[") and text.endswith("\\]"):
        text = text[2:-2].strip()
    return text


def parse_expression(raw: str) -> dict:
    """
    Parse a math expression/equation. Two-layer approach:
    1. Try SymPy's LaTeX parser (handles complex LaTeX natively)
    2. Fall back to manual clean_ocr_text + sympify
    """
    logger.info(f"Parsing expression: {raw[:80]}...")

    # Strip LaTeX delimiters first
    stripped = _strip_latex_delimiters(raw)

    # === Layer 1: Try parse_latex (handles \frac, \sqrt, \cos, etc.) ===
    try:
        if "=" in stripped:
            parts = stripped.split("=", 1)
            lhs_expr = latex2sympy(parts[0].strip())
            rhs_expr = latex2sympy(parts[1].strip())
            logger.info(f"LaTeX parsed as equation: {lhs_expr} = {rhs_expr}")
            return {
                "type": "equation",
                "lhs": lhs_expr,
                "rhs": rhs_expr,
                "raw": stripped
            }
        else:
            expr = latex2sympy(stripped)
            logger.info(f"LaTeX parsed as expression: {expr}")
            return {
                "type": "expression",
                "expr": expr,
                "raw": stripped
            }
    except Exception as latex_err:
        logger.warning(f"LaTeX parser failed: {latex_err}, trying manual cleanup")

    # === Layer 2: Fallback to manual clean + sympify ===
    try:
        cleaned = clean_ocr_text(raw)

        if "=" in cleaned:
            parts = cleaned.split("=")
            lhs_expr = sp.sympify(parts[0])
            rhs_expr = sp.sympify(parts[-1])
            logger.info(f"Manual parsed as equation: {lhs_expr} = {rhs_expr}")
            return {
                "type": "equation",
                "lhs": lhs_expr,
                "rhs": rhs_expr,
                "raw": cleaned
            }
        else:
            expr = sp.sympify(cleaned)
            logger.info(f"Manual parsed as expression: {expr}")
            return {
                "type": "expression",
                "expr": expr,
                "raw": cleaned
            }

    except Exception as e:
        logger.error(f"Both parsers failed: {str(e)}")
        raise ParserError(f"Failed to parse: {stripped}", details={"raw": raw, "stripped": stripped})