# 🧠 Math Problem Solver (Multi-Agent AI System)

An advanced **AI-powered math problem solver** built using a **multi-agent architecture** that mimics human problem-solving by breaking tasks into structured stages like OCR, parsing, solving, and verification.

---

## 🚀 Why This Project?

Traditional math solvers either:
- Depend heavily on LLMs (can hallucinate ❌)
- Or only use symbolic methods (limited flexibility ❌)

👉 This project combines **AI + symbolic reasoning + verification**  
to build a **robust and reliable math-solving system**.

---

## 🧠 System Architecture
Input (Image / Text)
->
🧾 OCR Agent
->
🧩 Parser Agent
->
🧮 Solver Agent
->
✅ Verifier Agent
->
🎯 Final Answer


---

## ⚙️ Core Components

### 1️⃣ OCR Agent
- Extracts mathematical text from images
- Uses OCR models (RapidOCR / Transformers)

### 2️⃣ Parser Agent
- Converts raw text into structured mathematical expressions
- Prepares input for symbolic solving

### 3️⃣ Solver Agent
- Uses **SymPy** for symbolic computation
- Solves equations and expressions

### 4️⃣ Verifier Agent
- Validates correctness of the solution
- Ensures reliability of output

---

## 🧩 Project Structure
```
Math-problem-solver/
│
├── src/
│ ├── agents/
│ │ ├── ocr_agent.py
│ │ ├── parser_agent.py
│ │ ├── solver_agent.py
│ │ └── verifier_agent.py
│ │
│ ├── symbolic/
│ ├── utils/
│ └── config/
│
├── tests/
│ ├── test_ocr.py
│ └── test_pipeline.py
│
├── requirements.txt
└── README.md
```


---

## 🛠️ Tech Stack

- 🐍 Python  
- 🔢 SymPy (Symbolic Mathematics)  
- 🤖 Transformers / OCR models  
- 📷 OpenCV  
- 🧠 Multi-Agent System Design

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
