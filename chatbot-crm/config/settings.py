import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GPT_MODEL = "gpt-4-turbo"
    CRM_DATA_PATH = "data/clients.json"
    OPENAI_API_TIMEOUT = 15  # Таймаут запроса в секундах

settings = Settings()