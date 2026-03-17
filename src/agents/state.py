from typing import TypedDict, Optional, Any

class PipelineState(TypedDict, total=False):
    """
    Shared state that flows through all agents in the pipeline.
    
    Each agent reads what it needs and adds its results.
    `total=False` means all fields are optional (they get filled as the pipeline runs).
    """
    
    # --- Input ---
    image_path: str              # The uploaded image path
    
    # --- OCR Agent output ---
    ocr_text: str                # Raw text extracted from image
    ocr_confidence: float        # How confident the OCR is (0.0–1.0)
    ocr_source: str              # "pix2text" or "llm_vision"
    
    # --- Parser output ---
    parsed: dict                 # {"type": "equation", "lhs": ..., "rhs": ...}
    
    # --- Classifier Agent output ---
    problem_type: str            # "algebra", "calculus_derivative", etc.
    
    # --- Solver Agent output ---
    llm_solution: str            # Raw LLM response (step-by-step text)
    sympy_solution: dict         # SymPy result: {"steps": [...], "answer": ...}
    
    # --- Verifier Agent output ---
    verification: dict           # {"verified": True/False, "details": [...]}
    
    # --- Final ---
    error: Optional[str]         # Error message if something went wrong
