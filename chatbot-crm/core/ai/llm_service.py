import requests
import logging
from config.settings import settings
from core.crm.models import Client
from config.prompts import RESPONSE_PROMPT_TEMPLATE

logger = logging.getLogger("LLMService")

class LLMService:
    def __init__(self):
        # Ваш ключ OpenRouter (лучше хранить в .env)
        self.api_key = "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"
        self.base_url = "https://openrouter.ai/api/v1"
    
    def generate_response(self, query: str, client: Client) -> str:
        prompt = RESPONSE_PROMPT_TEMPLATE.format(
            name=client.name,
            last_purchase=client.last_purchase,
            budget=client.budget,
            status_emoji=client.status_emoji,
            status_text=client.status_text,
            status_description=client.status_description,
            query=query
        )
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://premium-motors.ru",  # Ваш сайт
                "X-Title": "Premium Motors Bot"  # Название приложения
            }
            
            payload = {
                "model": "anthropic/claude-3-haiku",  # Лучшая модель для русского
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 200,
                "transformers": {
                    "middleware": [
                        {"name": "trim"}
                    ]
                }
            }
            
            logger.debug(f"Sending request to OpenRouter: {payload}")
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            else:
                error_msg = f"OpenRouter error: {response.status_code} - {response.text}"
                logger.error(error_msg)
                raise Exception(error_msg)
        
        except Exception as e:
            logger.error(f"⚠️ Ошибка генерации ответа: {str(e)}")
            return self.fallback_response(client, query)
    
    def fallback_response(self, client: Client, query: str) -> str:
        """Запасной ответ при ошибках"""
        return f"✨ {client.name}, спасибо за ваш запрос! " \
               f"Учитывая ваш интерес к {query} и историю с {client.last_purchase}, " \
               f"наш менеджер свяжется с вами в течение 5 минут."