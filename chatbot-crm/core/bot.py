from core.crm.repository import CRMRepository
from core.ai.llm_service import LLMService

class ChatBot:
    def __init__(self):
        self.crm_repo = CRMRepository()
        self.llm_service = LLMService()
    
    def process_request(self, client_name: str, query: str) -> str:
        client = self.crm_repo.find_client_by_name(client_name)
        if not client:
            return "❌ Клиент не найден в системе. Пожалуйста, проверьте данные."
        
        return self.llm_service.generate_response(query, client)