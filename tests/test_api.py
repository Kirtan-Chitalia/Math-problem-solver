import pytest
import os
from fastapi.testclient import TestClient
from src.api.app import app

client = TestClient(app)

def test_health():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_solve_endpoint():
    """Test the file upload and pipeline execution via API."""
    test_image = "data/image.png"
    
    # Skip test if image doesn't exist
    if not os.path.exists(test_image):
        pytest.skip(f"Test image {test_image} not found")
        
    with open(test_image, "rb") as f:
        response = client.post(
            "/solve",
            files={"file": ("image.png", f, "image/png")}
        )
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify the schema fields exist
    assert "ocr_text" in data
    assert "problem_type" in data
    assert "llm_solution" in data
