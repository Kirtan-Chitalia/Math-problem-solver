# End-to-End Build Roadmap — Math Solver Multiagent

> All files are empty scaffolds. This guide tells you what to put in each one, in order.

---

## Your Project Structure

```
src/
├── main.py                    ← Entry point (do this LAST)
├── vision/
│   └── ocr.py                 ← Step 1: Image → text
├── symbolic/
│   ├── parser.py              ← Step 2: text → SymPy expression
│   ├── solver.py              ← Step 3: expression → solution
│   └── verifier.py            ← Step 4: verify the answer
└── agents/
    ├── planner.py             ← Step 5: classify problem type
    ├── algerbra_agent.py      ← Step 6a: algebra-specific logic
    ├── calculus_agent.py      ← Step 6b: calculus-specific logic
    └── superviser.py          ← Step 7: LangGraph orchestrator
```

---

## Build Order

### ✅ Step 1 — `src/vision/ocr.py`

**What it does:** Takes an image path → returns a string of the math expression

**Libraries to import:** `cv2`, `numpy`, `PIL.Image`, `pix2text` (or `easyocr`)

**What to write:**

1. A function `preprocess_image(image_path: str) -> np.ndarray`
   - Load the image with `cv2.imread()`
   - Convert to grayscale: `cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)`
   - Apply thresholding: `cv2.threshold()` with `THRESH_BINARY + THRESH_OTSU`
   - Return the cleaned image

2. A function `extract_text(image_path: str) -> str`
   - Call `preprocess_image()` first
   - Initialize Pix2Text: `p2t = Pix2Text.from_config()`
   - Run OCR: `result = p2t(image_path)`
   - Return the extracted string (e.g. `"x^2 + 3x - 4 = 0"`)

**Test it:** Pass a sample image from `data/formula_images_processed/`, print the result. Does it return the equation?

---

### ✅ Step 2 — `src/symbolic/parser.py`

**What it does:** Takes the raw OCR string → returns a SymPy expression

**Libraries:** `sympy`, `re`

**What to write:**

1. A function `clean_ocr_text(raw: str) -> str`
   - Replace common OCR mistakes:
     - `^` → `**`
     - `×` → `*`
     - `÷` → `/`
     - `²` → `**2`, `³` → `**3`
     - Remove stray spaces around operators
   - Handle implicit multiplication: `"2x"` → `"2*x"` using regex `r'(\d)([a-zA-Z])'` → `r'\1*\2'`

2. A function `parse_expression(raw: str) -> tuple`
   - Call `clean_ocr_text(raw)` 
   - Split on `=` if equation: `lhs, rhs = cleaned.split("=")`
   - Use `sympy.parse_expr(lhs)` and `sympy.parse_expr(rhs)`
   - Return `(lhs_expr, rhs_expr)` or just `(expr, None)` if no `=`

**Test it:** Feed in `"x^2 + 3x - 4 = 0"`, check you get a proper SymPy equation back.

---

### ✅ Step 3 — `src/symbolic/solver.py`

**What it does:** Takes the SymPy expression + problem type → returns solution steps

**Libraries:** `sympy`

**What to write:**

1. A function `solve_algebra(lhs, rhs, variable="x") -> dict`
   - Create equation: `eq = sympy.Eq(lhs, rhs)`
   - Solve: `solutions = sympy.solve(eq, sympy.Symbol(variable))`
   - Return `{"steps": [...], "answer": solutions}`

2. A function `solve_calculus_derivative(expr, variable="x") -> dict`
   - Compute: `result = sympy.diff(expr, sympy.Symbol(variable))`
   - Return `{"steps": ["Applied differentiation rules"], "answer": result}`

3. A function `solve_calculus_integral(expr, variable="x") -> dict`
   - Compute: `result = sympy.integrate(expr, sympy.Symbol(variable))`
   - Return `{"steps": ["Applied integration rules"], "answer": result}`

4. A dispatcher function `solve(expr_tuple: tuple, problem_type: str) -> dict`
   - Based on `problem_type`, call the right function above
   - Return the result dict

**Test it:** Create a SymPy expression manually, call `solve()`, print steps and answer.

---

### ✅ Step 4 — `src/symbolic/verifier.py`

**What it does:** Checks if the solution is correct by substituting back

**Libraries:** `sympy`

**What to write:**

1. A function `verify(original_lhs, original_rhs, solution: dict) -> dict`
   - Get the answer from `solution["answer"]`
   - For each answer value, substitute into the original equation:
     `result = (original_lhs - original_rhs).subs(x, answer_val)`
   - Simplify: `sympy.simplify(result)`
   - If it equals `0` → verified ✅
   - Return `{"verified": True/False, "details": ...}`

---

### ✅ Step 5 — `src/agents/planner.py`

**What it does:** Takes the parsed expression string → identifies problem type

**This is your Classifier Agent.**

**Libraries:** `re`, `sympy` (optional: an LLM via `langchain-core`)

**What to write:**

1. A function `classify_problem(raw_text: str) -> str`
   - Check for keywords using regex or `.find()`:
     - `"integrate"` or `"∫"` → `"calculus_integral"`
     - `"d/dx"` or `"differentiat"` or `"'"` → `"calculus_derivative"`
     - `"sin"`, `"cos"`, `"tan"` → `"trigonometry"`
     - `"matrix"`, `"determinant"` → `"linear_algebra"`
     - `"="` with polynomial → `"algebra"`
   - Default: `"algebra"`
   - Return the category string

**Test it:** Pass `"integrate x^2 dx"` → should return `"calculus_integral"`

---

### ✅ Step 6a — `src/agents/algerbra_agent.py`

**What it does:** Wraps the algebra solve path into an agent-style callable

**What to write:**

1. A function `run_algebra_agent(state: dict) -> dict`
   - `state` is the shared pipeline dictionary (more on this in Step 7)
   - Pull out `state["expression"]` (the parsed SymPy tuple)
   - Call `solver.solve(expression, "algebra")`
   - Call `verifier.verify(...)` with the result
   - Add results back to state: `state["solution"] = ...`, `state["verified"] = ...`
   - Return the updated `state`

**Why this shape?** LangGraph nodes are functions that take a state dict and return an updated state dict.

---

### ✅ Step 6b — `src/agents/calculus_agent.py`

**Same pattern as algebra_agent but for calculus:**

1. A function `run_calculus_agent(state: dict) -> dict`
   - Check `state["problem_type"]` for `"calculus_derivative"` or `"calculus_integral"`
   - Call appropriate solver function
   - Update and return state

---

### ✅ Step 7 — `src/agents/superviser.py`

**What it does:** Wires everything into a LangGraph pipeline

**This is the Orchestrator / Supervisor.**

**Libraries:** `langgraph.graph`, your other modules

**What to write:**

1. Define the **state schema** as a `TypedDict`:
   ```python
   class PipelineState(TypedDict):
       image_path: str
       raw_text: str
       expression: tuple
       problem_type: str
       solution: dict
       verified: dict
   ```

2. Define **node functions** (one per agent):
   - `vision_node(state)` → calls `ocr.extract_text()`, stores in `state["raw_text"]`
   - `parser_node(state)` → calls `parser.parse_expression()`, stores in `state["expression"]`
   - `planner_node(state)` → calls `planner.classify_problem()`, stores `state["problem_type"]`
   - `solver_node(state)` → routes to algebra or calculus agent based on `problem_type`
   - `verifier_node(state)` → calls `verifier.verify()`, stores result

3. **Build the graph:**
   ```python
   graph = StateGraph(PipelineState)
   graph.add_node("vision", vision_node)
   graph.add_node("parser", parser_node)
   # ... add all nodes
   graph.add_edge("vision", "parser")
   graph.add_edge("parser", "planner")
   # conditional edge for algebra vs calculus:
   graph.add_conditional_edges("planner", route_by_type, {
       "algebra": "algebra_solver",
       "calculus_derivative": "calculus_solver",
       ...
   })
   graph.set_entry_point("vision")
   pipeline = graph.compile()
   ```

4. A function `run_pipeline(image_path: str) -> dict`
   - Calls `pipeline.invoke({"image_path": image_path})`
   - Returns the final state

---

### ✅ Step 8 — `src/main.py`

**What it does:** Entry point — accepts image path from CLI and prints results

**What to write:**

1. Parse CLI argument: `image_path = sys.argv[1]`
2. Call `superviser.run_pipeline(image_path)`
3. Use `rich` to pretty-print the results:
   - Extracted equation
   - Problem type
   - Steps
   - Final answer
   - Verified: ✅ or ❌

---

## Data Flow Summary

```
image_path
    │
    ▼
[vision_node]      ocr.extract_text()         → raw_text
    │
    ▼
[parser_node]      parser.parse_expression()  → expression (SymPy tuple)
    │
    ▼
[planner_node]     planner.classify_problem() → problem_type
    │
    ▼
[solver_node]      algebra_agent OR           → solution dict
                   calculus_agent
    │
    ▼
[verifier_node]    verifier.verify()          → verified dict
    │
    ▼
[main.py output]   rich.print(...)
```

---

## What Each `__init__.py` Should Export

Each `__init__.py` is currently empty. Add these imports:

- `src/vision/__init__.py` → `from .ocr import extract_text`
- `src/symbolic/__init__.py` → `from .parser import parse_expression` `from .solver import solve` `from .verifier import verify`
- `src/agents/__init__.py` → `from .superviser import run_pipeline`
- `src//__init__.py` → leave empty or add version string

---

## Build Sequence Summary

| Order | File | Dependency |
|-------|------|------------|
| 1 | `vision/ocr.py` | None |
| 2 | `symbolic/parser.py` | `ocr.py` output |
| 3 | `symbolic/solver.py` | `parser.py` output |
| 4 | `symbolic/verifier.py` | `solver.py` output |
| 5 | `agents/planner.py` | `parser.py` output |
| 6 | `agents/algerbra_agent.py` | `solver.py`, `verifier.py` |
| 6 | `agents/calculus_agent.py` | `solver.py`, `verifier.py` |
| 7 | `agents/superviser.py` | All above |
| 8 | `main.py` | `superviser.py` |

---

## Tips While Coding

> [!TIP]
> Work **file by file** and test each one in isolation before moving on. Use `python -c "from src.vision.ocr import extract_text; print(extract_text('data/sample.png'))"` to test quickly.

> [!NOTE]
> The `state` dict in LangGraph flows through every node — each node reads from it and adds to it. Think of it like a shared clipboard that gets richer as it passes through each agent.

> [!IMPORTANT]
> Pix2Text will download model weights on first run (~500MB). Make sure your internet is connected when you first call `Pix2Text.from_config()`.

> [!WARNING]
> Your file is named `algerbra_agent.py` (typo — "algerbra" not "algebra"). Keep the filename as-is to avoid import errors, but use the correct spelling inside the code.
