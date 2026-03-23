from src.agents.orchestrator import run_pipeline

image_path = "data/image.png"  # Replace with your test image path

print("=" * 60)
print("FULL PIPELINE TEST")
print("=" * 60)

result = run_pipeline(image_path)

print(f"\n📷 Image: {result.get('image_path')}")
print(f"📝 OCR Text: {result.get('ocr_text')}")
print(f"🔍 OCR Source: {result.get('ocr_source')} (confidence: {result.get('ocr_confidence', 0):.2f})")
print(f"📂 Problem Type: {result.get('problem_type')}")
print(f"\n🧮 LLM Solution:\n{result.get('llm_solution', 'N/A')}")
print(f"\n🔢 SymPy Answer: {result.get('sympy_solution', {}).get('answer', 'N/A')}")
print(f"✅ Verified: {result.get('verification', {}).get('verified', 'N/A')}")

if result.get("error"):
    print(f"\n⚠️ Error: {result['error']}")

print("=" * 60)
