from pydantic import BaseModel
from typing import Optional


class SolveRequest(BaseModel):
    """What the user sends to the API."""
    image_path: str  # Path to the math image


class SolveResponse(BaseModel):
    """What the API returns."""
    
    # OCR results
    ocr_text: str
    ocr_confidence: float
    ocr_source: str
    
    # Classification
    problem_type: str
    
    # Solution
    llm_solution: str
    sympy_answer: Optional[str] = None  # str because SymPy objects aren't JSON-serializable
    
    # Verification
    verified: Optional[str] = None  # "True", "False", "skipped", "timeout"
    
    # Error
    error: Optional[str] = None