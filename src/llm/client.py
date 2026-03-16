import openai
from src.config import settings
from src.utils import get_logger , LLMError
import base64

logger = get_logger(__name__)

class LLMClient:
    def __init__(self):
        self.client = openai.OpenAI(
            api_key=settings.OPENROUTER_API_KEY,
            base_url=settings.OPENROUTER_BASE_URL,
        )
    def chat(self, prompt:str,model:str=None,system_prompt:str="") -> str:
        if model is None:
            model = settings.SOLVER_MODEL
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=1024,
                timeout=settings.LLM_TIMEOUT_SECONDS,
            )
            result = response.choices[0].message.content

            logger.info(f"LLM call successful | model={model}")
            logger.debug(f"Response preview: {result[:100]}")

            return result

        except Exception as e:
            logger.error(f"LLM call failed: {str(e)}")
            raise LLMError(f"LLM request failed: {str(e)}")
    


    def chat_with_image(self, prompt: str, image_path: str, model: str = None) -> str:

        if model is None:
            model = settings.VISION_MODEL

        try:

            with open(image_path, "rb") as img_file:
                image_bytes = img_file.read()

            image_base64 = base64.b64encode(image_bytes).decode("utf-8")

            content = [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{image_base64}"
                    },
                },
            ]

            messages = [
                {
                    "role": "user",
                    "content": content
                }
            ]

            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=1024,
                timeout=settings.LLM_TIMEOUT_SECONDS,
            )

            result = response.choices[0].message.content

            logger.info(f"Vision LLM call | model={model}")
            logger.debug(f"Response preview: {result[:100]}")

            return result

        except Exception as e:
            logger.error(f"Vision LLM call failed: {str(e)}")
            raise LLMError(f"Vision request failed: {str(e)}")