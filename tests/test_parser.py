from src.symbolic.parser import parse_expression

# Test 1: Equation
print("=" * 50)
print("TEST 1: Equation")
result = parse_expression("x^2 + 3x - 4 = 0")
print(f"  Type: {result['type']}")
print(f"  LHS: {result['lhs']}")
print(f"  RHS: {result['rhs']}")

# Test 2: Expression (no =)
print("=" * 50)
print("TEST 2: Expression")
result = parse_expression("\\frac{x}{2} + 3")
print(f"  Type: {result['type']}")
print(f"  Expr: {result['expr']}")

# Test 3: Bad input (should raise ParserError)
print("=" * 50)
print("TEST 3: Bad input")
try:
    result = parse_expression("@#$%&!!!")
except Exception as e:
    print(f"  ✅ Caught: {type(e).__name__}: {e}")

print("=" * 50)
