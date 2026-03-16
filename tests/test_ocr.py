from src.vision.ocr import extract_text
print("="*50)
print("test 1 :image validation")
image_path = "data/formula_images_processed/formula_images_processed/ffc121051d.png"
result = extract_text(image_path)
print(f"Extracted text: {result}")
print(f"  Confidence: {result['confidence']:.2f}")
print(f"  Source: {result['source']}")

print("=" * 50)
print("TEST 2: Non-existent image")
try:
    result = extract_text("data/fake_image.png")
    print("  ❌ Should have raised OCRError!")
except Exception as e:
    print(f"  ✅ Caught error: {type(e).__name__}: {e}")

print("=" * 50)
print("TEST 3: Confidence estimation")
from src.vision.ocr import _estimate_confidence
print(f"  'x^2 + 3x = 0' → {_estimate_confidence('x^2 + 3x = 0'):.2f}")
print(f"  '' (empty) → {_estimate_confidence(''):.2f}")
print(f"  'hello world' → {_estimate_confidence('hello world'):.2f}")
print(f"  'ab' (too short) → {_estimate_confidence('ab'):.2f}")
print("=" * 50)

# --- Test 4: LLM Vision fallback ---
print("=" * 50)
print("TEST 4: LLM Vision OCR")
from src.vision.llm_vision import extract_text_with_llm
result = extract_text_with_llm(image_path)
print(f"  Text: {result['text']}")
print(f"  Confidence: {result['confidence']}")
print(f"  Source: {result['source']}")
print("=" * 50)
