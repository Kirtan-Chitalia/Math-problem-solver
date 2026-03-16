import sympy as sp
from src.symbolic.solver import solve
from src.symbolic.verifier import verify

# Test 1: Correct algebra answer
print("=" * 50)
print("TEST 1: Correct algebra answer")
parsed = {"lhs": sp.sympify("x**2 + 3*x - 4"), "rhs": sp.sympify("0")}
solution = solve(parsed, "algebra")
result = verify(parsed, solution)
print(f"  Verified: {result['verified']}")
print(f"  Details: {result['details']}")

# Test 2: Wrong answer (manually inject bad answer)
print("=" * 50)
print("TEST 2: Wrong answer")
parsed = {"lhs": sp.sympify("x**2 + 3*x - 4"), "rhs": sp.sympify("0")}
bad_solution = {"steps": ["Guessed"], "answer": [5, 10]}
result = verify(parsed, bad_solution)
print(f"  Verified: {result['verified']}")
print(f"  Details: {result['details']}")

# Test 3: Derivative verification
print("=" * 50)
print("TEST 3: Derivative verification")
parsed = {"expr": sp.sympify("x**3 + 2*x")}
solution = solve(parsed, "calculus_derivative")
result = verify(parsed, solution)
print(f"  Verified: {result['verified']}")
print(f"  Details: {result['details']}")

# Test 4: Integral verification
print("=" * 50)
print("TEST 4: Integral verification")
parsed = {"expr": sp.sympify("x**2 + 1")}
solution = solve(parsed, "calculus_integral")
result = verify(parsed, solution)
print(f"  Verified: {result['verified']}")
print(f"  Details: {result['details']}")

print("=" * 50)
