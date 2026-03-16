import sympy as sp
from src.symbolic.solver import solve

# Test 1: Algebra
print("=" * 50)
print("TEST 1: Algebra — x^2 + 3x - 4 = 0")
parsed = {"type": "equation", "lhs": sp.sympify("x**2 + 3*x - 4"), "rhs": sp.sympify("0")}
result = solve(parsed, "algebra")
print(f"  Steps: {result['steps']}")
print(f"  Answer: {result['answer']}")

# Test 2: Derivative
print("=" * 50)
print("TEST 2: Derivative — d/dx(x^3 + 2x)")
parsed = {"type": "expression", "expr": sp.sympify("x**3 + 2*x")}
result = solve(parsed, "calculus_derivative")
print(f"  Steps: {result['steps']}")
print(f"  Answer: {result['answer']}")

# Test 3: Integral
print("=" * 50)
print("TEST 3: Integral — ∫(x^2 + 1)dx")
parsed = {"type": "expression", "expr": sp.sympify("x**2 + 1")}
result = solve(parsed, "calculus_integral")
print(f"  Steps: {result['steps']}")
print(f"  Answer: {result['answer']}")

# Test 4: Unsupported type
print("=" * 50)
print("TEST 4: Unsupported type")
try:
    solve({}, "quantum_physics")
except Exception as e:
    print(f"  ✅ Caught: {type(e).__name__}: {e}")

print("=" * 50)
