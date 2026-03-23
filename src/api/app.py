from fastapi import FastAPI, UploadFile, File, HTTPException
from src.api.schemas import SolveResponse
from src.agents.orchestrator import run_pipeline
from src.utils import get_logger

import shutil
import os
import uuid

logger = get_logger(__name__)

app = FastAPI(
    title="AI Math Solver",
    description="Upload a math image → get step-by-step solution",
    version="1.0.0"
)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/solve", response_model=SolveResponse)
async def solve(file: UploadFile = File(...)):
    """
    Upload a math image and get the solution.
    """

    temp_dir = "data/uploads"
    os.makedirs(temp_dir, exist_ok=True)

    temp_path = os.path.join(
        temp_dir,
        f"{uuid.uuid4()}_{file.filename}"
    )

    try:
        # -------------------------------
        # 1. Save uploaded file
        # -------------------------------
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info(f"Saved upload to {temp_path}")

        # -------------------------------
        # 2. Run AI pipeline
        # -------------------------------
        result = run_pipeline(temp_path)

        # -------------------------------
        # 3. Build API response
        # -------------------------------
        response = SolveResponse(
            ocr_text=result.get("ocr_text", ""),
            ocr_confidence=result.get("ocr_confidence", 0.0),
            ocr_source=result.get("ocr_source", ""),
            problem_type=result.get("problem_type", ""),
            llm_solution=result.get("llm_solution", ""),
            sympy_answer=str(result.get("sympy_solution", {}).get("answer")),
            verified=str(result.get("verification", {}).get("verified")),
            error=result.get("error")
        )

        return response

    except Exception as e:
        logger.exception("Pipeline failed")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # -------------------------------
        # 4. Cleanup temp file
        # -------------------------------
        if os.path.exists(temp_path):
            os.remove(temp_path)
            logger.info(f"Deleted temp file {temp_path}")