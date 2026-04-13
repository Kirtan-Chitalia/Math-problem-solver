# 🧠 Math Problem Solver (Multi-Agent AI System)

An advanced AI-powered math problem solver built using a **multi-agent architecture** that mimics human problem-solving by breaking tasks into structured stages — OCR extraction, classification, solving, and verification.

> **Why is this different?** Traditional math solvers either depend heavily on LLMs (prone to hallucinations) or use only symbolic methods (limited flexibility). This project combines **AI reasoning + symbolic computation + verification** to build a robust, interpretable, and reliable system.

---

## 🎯 Example

**Input:** An image containing a math problem

**Output:**
```
📝 OCR: 2x + 3 = 7
📂 Type: algebraic_equation
🧮 Solution:
  Step 1: Subtract 3 from both sides → 2x = 4
  Step 2: Divide by 2 → x = 2
🔢 SymPy Answer: [2]
✅ Verified: True
```

---

## 🧠 System Architecture

```
Input (Image)
      ↓
🧾 OCR Agent ──────────── Pix2Text (local) / LLM Vision (fallback)
      ↓
🏷️ Classifier Agent ───── Claude Sonnet (problem type detection)
      ↓
🧮 Solver Agent ────────── DeepSeek v3.2 (steps) + SymPy (symbolic answer)
      ↓
✅ Verifier Agent ──────── SymPy re-computation & cross-check
      ↓
🎯 Final Answer (JSON)
```

### Agent Communication

Each agent operates sequentially via a **LangGraph StateGraph**, sharing a common `PipelineState`:

```json
{
  "image_path": "data/image.png",
  "ocr_text": "2x + 3 = 7",
  "ocr_confidence": 0.95,
  "ocr_source": "pix2text",
  "problem_type": "algebraic_equation",
  "llm_solution": "Step 1: Subtract 3...\nStep 2: Divide by 2...",
  "sympy_solution": {"answer": "[2]", "steps": ["..."]},
  "verification": {"verified": true}
}
```

---

## 📂 Project Structure

```
Math-problem-solver/
├── data/                       # Test images and uploads
├── notebooks/                  # Jupyter notebooks for experimentation
├── src/
│   ├── agents/                 # Multi-agent system
│   │   ├── ocr_agent.py        # OCR extraction with fallback
│   │   ├── classifier_agent.py # Problem type classification
│   │   ├── solver_agent.py     # Hybrid LLM + SymPy solver
│   │   ├── verifier_agent.py   # Solution verification
│   │   ├── orchestrator.py     # LangGraph pipeline
│   │   └── state.py            # Shared pipeline state
│   ├── api/                    # FastAPI web service
│   │   ├── app.py              # API routes (/solve, /health)
│   │   └── schemas.py          # Pydantic request/response models
│   ├── config/                 # App configuration
│   │   └── settings.py         # Environment-based settings
│   ├── llm/                    # LLM integration
│   │   ├── client.py           # OpenRouter API client
│   │   └── prompts.py          # Prompt templates
│   ├── symbolic/               # Symbolic math engine
│   │   ├── parser.py           # LaTeX → SymPy expression parser
│   │   ├── solver.py           # Algebra, calculus, trig solver
│   │   └── verifier.py         # Solution re-computation
│   ├── utils/                  # Logging, error handling
│   └── vision/                 # Image processing
│       ├── ocr.py              # Pix2Text OCR with confidence scoring
│       └── llm_vision.py       # LLM Vision fallback OCR
├── tests/                      # Unit and integration tests
├── main.py                     # CLI entry point (serve / solve)
├── requirements.txt
└── README.md
```

---

## ⚙️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.10+ |
| **OCR (Primary)** | Pix2Text (local, free) |
| **OCR (Fallback)** | GPT-4.1 Mini via OpenRouter |
| **Classifier** | Claude Sonnet 4.6 via OpenRouter |
| **Solver (LLM)** | DeepSeek v3.2 via OpenRouter |
| **Solver (Symbolic)** | SymPy |
| **LaTeX Parser** | latex2sympy2 + manual fallback |
| **Multi-Agent Framework** | LangGraph (StateGraph) |
| **API** | FastAPI + Uvicorn |
| **Image Processing** | OpenCV, Pillow |

---

## ▶️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Kirtan-Chitalia/Math-problem-solver.git
cd Math-problem-solver
```

### 2. Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

Get your API key from [OpenRouter](https://openrouter.ai/).

---

## ▶️ Usage

### CLI — Solve from Image

```bash
python main.py solve data/image.png
```

### API Server

Start the FastAPI server:

```bash
python main.py serve
```

Then open **http://localhost:8000/docs** for the interactive Swagger UI.

### API — cURL Example

```bash
curl -X POST http://localhost:8000/solve \
  -F "file=@data/image.png"
```

### API Response

```json
{
  "ocr_text": "\\frac{dx}{4x^2-1}=A\\log\\left(\\frac{2x-1}{2x+1}\\right)+c",
  "ocr_confidence": 1.0,
  "ocr_source": "pix2text",
  "problem_type": "calculus_integral",
  "llm_solution": "Step 1: Factor 4x²-1 = (2x-1)(2x+1)...",
  "sympy_answer": "1/4",
  "verified": "True",
  "error": null
}
```

---

## ✅ Supported Problem Types

| Type | Examples |
|------|---------|
| **Algebraic Equations** | `2x + 3 = 7`, `x² - 5x + 6 = 0` |
| **Derivatives** | `d/dx(x³ + 2x)`, `y = e^(5x)` |
| **Integrals** | `∫ dx/(4x²-1)`, `∫ sin(x) dx` |
| **Trigonometric** | `sin²θ + cos²θ = 1` |
| **Simplification** | `(x² - 1)/(x - 1)` |

---

## 🔁 Fault Tolerance

| Layer | Fallback Strategy |
|-------|------------------|
| **OCR** | Pix2Text → LLM Vision (when confidence < 0.7) |
| **Parser** | latex2sympy2 → manual cleanup + sympify |
| **LLM** | Null response detection with proper error handling |
| **Verification** | Timeout handling for complex expressions |

---

## 🧪 Testing

Run all tests:

```bash
pytest tests/ -v
```

Run specific tests:

```bash
pytest tests/test_api.py -v        # API endpoint tests
python -m tests.test_pipeline      # Full pipeline test
```

---

## ⚠️ Known Limitations

- Complex handwritten math may produce low-confidence OCR
- Word problems are not fully supported
- Some non-standard LaTeX notation may cause parsing issues
- SymPy cannot solve all problem types (LLM solution is always provided as fallback)

---

## 🚀 Future Improvements

- 🌐 **Web UI** — React/Next.js frontend with LaTeX rendering
- 📷 **Handwritten math** — Fine-tuned OCR for handwriting
- 🧠 **Hybrid solver** — LLM-guided SymPy strategies
- 🌍 **Multilingual** — Support for non-English math notation
- 📊 **Benchmarking** — Automated accuracy testing on standard datasets
- 🧩 **Plug-and-play agents** — Add new problem-type agents easily

---

## ⭐ Why This Project Stands Out

- **Multi-agent AI architecture** — Not just a wrapper around an LLM
- **Hybrid reasoning** — Combines symbolic (SymPy) + neural (LLM) approaches
- **Built-in verification** — Rare in student projects; catches LLM hallucinations
- **Production-grade patterns** — Logging, error handling, API design, testing
- **Modular & extensible** — Easy to add new agents or swap LLM providers

---


---

*Built by [Kirtan Chitalia](https://github.com/Kirtan-Chitalia)*
