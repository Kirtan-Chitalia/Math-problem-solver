# 🧠 Math Problem Solver (Multi-Agent AI System)

An advanced AI-powered math problem solver built using a **multi-agent architecture** that mimics human problem-solving by breaking tasks into structured stages like OCR, parsing, solving, and verification.

---

## 🚀 Overview

Traditional math solvers typically:

* Depend heavily on Large Language Models → prone to hallucinations ❌
* Use only symbolic methods → limited flexibility ❌

👉 This project combines **AI + symbolic reasoning + verification**
to build a **robust, interpretable, and reliable math-solving system**.

---

## 🎯 Example

**Input (Text):**

```
2x + 3 = 7
```

**Output:**

```
Step 1: Subtract 3 from both sides → 2x = 4  
Step 2: Divide by 2 → x = 2  

✅ Verified: Solution is correct
```

---

## 🧠 System Architecture

```
Input (Image / Text)
        ↓
🧾 OCR Agent
        ↓
🧩 Parser Agent
        ↓
🧮 Solver Agent
        ↓
✅ Verifier Agent
        ↓
🎯 Final Answer
```

---

## 🔄 Agent Workflow

Each agent operates sequentially and communicates via structured data:

1. **OCR Agent**

   * Extracts mathematical text from images
2. **Parser Agent**

   * Converts raw text into structured expressions
3. **Solver Agent**

   * Solves equations using symbolic computation
4. **Verifier Agent**

   * Re-validates the solution for correctness

### 📦 Data Flow (Example)

```json
{
  "input": "2x + 3 = 7",
  "parsed": "Eq(2*x + 3, 7)",
  "solution": "x = 2",
  "verified": true,
  "confidence": 0.94
}
```

---

## ⚙️ Core Components

### 🧾 OCR Agent

* Extracts mathematical text from images
* Supports RapidOCR / Transformer-based OCR models

### 🧩 Parser Agent

* Converts text into structured mathematical expressions
* Handles tokenization and normalization

### 🧮 Solver Agent

* Uses **SymPy** for symbolic computation
* Solves algebraic expressions and equations

### ✅ Verifier Agent

* Validates correctness of solutions
* Re-substitutes results to ensure accuracy

---

## 🛠️ Tech Stack

* 🐍 Python
* 🔢 SymPy (Symbolic Mathematics)
* 🤖 Transformers / OCR Models
* 📷 OpenCV
* 🧠 Multi-Agent System Design

---

## 📂 Project Structure

```
Math-problem-solver/
│
├── src/
│   ├── agents/
│   │   ├── ocr_agent.py
│   │   ├── parser_agent.py
│   │   ├── solver_agent.py
│   │   └── verifier_agent.py
│   │
│   ├── symbolic/
│   ├── utils/
│   └── config/
│
├── tests/
│   ├── test_ocr.py
│   └── test_pipeline.py
│
├── requirements.txt
└── README.md
```

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

---

## ▶️ Usage

### Run via CLI

```bash
python src/main.py --input "2x + 3 = 7"
```

### Modes (optional)

```bash
--mode explain   # step-by-step solution
--mode fast      # direct answer only
--debug true     # logs each agent step
```

---

## 🌐 API (Optional Extension)

```http
POST /solve
Content-Type: application/json

{
  "question": "2x + 3 = 7"
}
```

**Response:**

```json
{
  "answer": "x = 2",
  "steps": [...],
  "verified": true,
  "confidence": 0.94
}
```

---

## 📊 Evaluation

| Metric         | Value   |
| -------------- | ------- |
| Test Problems  | 100     |
| Accuracy       | ~85–90% |
| Avg Solve Time | ~0.1s   |

---

## ✅ Supported Problem Types

* Linear equations
* Quadratic equations
* Basic algebraic simplification
* Integration
* Differentiation
* Trigonometric equations
* And many more!

---

## ⚠️ Limitations

* Complex handwritten OCR may fail
* Word problems not fully supported
* Non-standard notation may cause parsing issues

---

## 🔁 Fault Tolerance

* OCR fallback for low-confidence extraction
* Parser fallback (rule-based → AI-based)
* Verification ensures correctness before output

---

## 🚀 Future Improvements

* 🧠 Hybrid solver (SymPy + LLM reasoning)
* 📷 Handwritten math recognition
* 🌍 Multilingual input support
* 📊 Advanced benchmarking dataset
* 🌐 Web UI (Next.js + FastAPI)
* 🧩 Plug-and-play agent architecture

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new branch
3. Commit changes
4. Submit a Pull Request

---

## ⭐ Why This Project Stands Out

* Multi-agent AI architecture
* Combines symbolic + AI reasoning
* Built-in verification layer (rare in student projects)
* Modular and extensible design

