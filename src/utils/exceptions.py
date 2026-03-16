"""
Custom exceptions for the AI Math Solver.

WHY CUSTOM EXCEPTIONS:
- Generic exceptions (ValueError, RuntimeError) make debugging harder
- Custom exceptions tell you EXACTLY what went wrong and WHERE in the pipeline
- Each pipeline stage has its own exception class
- The orchestrator can catch specific exceptions and decide how to handle them
  (e.g., OCRError → retry with LLM vision, SolverError → try a different approach)

HIERARCHY:
    MathSolverError          ← Base (catch-all for our app)
    ├── OCRError             ← Image processing / text extraction failed
    ├── ParserError          ← Could not parse OCR text into math expression
    ├── LLMError             ← OpenRouter API call failed
    ├── SolverError          ← Could not solve the equation
    └── VerificationError    ← Solution verification failed
"""


class MathSolverError(Exception):
    """Base exception for all Math Solver errors."""

    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message)
        self.details = details or {}


class OCRError(MathSolverError):
    """Raised when OCR fails to extract text from an image."""
    pass


class ParserError(MathSolverError):
    """Raised when the parser cannot convert text to a SymPy expression."""
    pass


class LLMError(MathSolverError):
    """Raised when the LLM API call fails (timeout, rate limit, bad response)."""
    pass


class SolverError(MathSolverError):
    """Raised when the solver cannot find a solution."""
    pass


class VerificationError(MathSolverError):
    """Raised when solution verification fails."""
    pass
