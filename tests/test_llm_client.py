from src.llm import LLMClient
from src.llm.prompts import PromptTemplates
from src.config import settings
from src.utils import get_logger
logger = get_logger(__name__)

print("="*50)
print("Test 1 : config")
print(f"Api key loaded: {'Yes' if settings.OPENROUTER_API_KEY else 'No'}")
print(f"Classifier model: {settings.CLASSIFIER_MODEL}")
print(f"Solver model: {settings.SOLVER_MODEL}")
print(f"Vision model: {settings.VISION_MODEL}")
print("Config Works")

print("="*50)
print("Test 2 : Logger")
logger.info("Logger test message")
print("Logger Works")

print("="*50)
print("Test 3 : classifier")
llm_client = LLMClient()
system = PromptTemplates.classifier_system_prompt()
user = PromptTemplates.classifier_user_prompt("x^2 + 3x - 4 = 0")
response = llm_client.chat(prompt=user, system_prompt=system)
model = settings.CLASSIFIER_MODEL
print(f"Input: x^2 + 3x - 4 = 0")
print(f"Classified as {response.strip()}")

print("="*50)
print("Test 4 : solver")
system = PromptTemplates.solver_system_prompt("algebra")
user = PromptTemplates.solver_user_prompt("x^2 + 3x - 4 = 0")
response = llm_client.chat(prompt=user, system_prompt=system)
model = settings.SOLVER_MODEL
print(f"Solution:\n{response}")

print("="*50)
