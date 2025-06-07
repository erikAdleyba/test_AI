import json
import logging
from typing import Optional
from core.crm.models import Client
from config.settings import settings

logger = logging.getLogger("CRM")

class CRMRepository:
    def __init__(self):
        self.clients = self._load_clients()
        logger.info(f"Загружено {len(self.clients)} клиентов")
    
    def _load_clients(self) -> list[Client]:
        try:
            with open(settings.CRM_DATA_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                clients = [Client(**client) for client in data["clients"]]
                logger.debug("Успешная загрузка данных CRM")
                return clients
        except FileNotFoundError:
            logger.error(f"Файл {settings.CRM_DATA_PATH} не найден!")
            return []
        except json.JSONDecodeError:
            logger.error(f"Ошибка в формате файла {settings.CRM_DATA_PATH}")
            return []
        except Exception as e:
            logger.error(f"Неизвестная ошибка при загрузке CRM: {str(e)}")
            return []
    
    # ДОБАВЛЯЕМ ОТСУТСТВУЮЩИЙ МЕТОД
    def find_client_by_name(self, name: str) -> Optional[Client]:
        """
        Улучшенный поиск клиента по имени:
        - Регистронезависимый
        - Частичное совпадение
        - Поиск по инициалам
        - Поиск только по имени или фамилии
        """
        if not name or not self.clients:
            return None
            
        search_term = name.strip().lower()
        
        # 1. Точное совпадение (полное имя)
        for client in self.clients:
            if search_term == client.name.lower():
                return client
        
        # 2. Частичное совпадение
        for client in self.clients:
            if search_term in client.name.lower():
                return client
        
        # 3. Поиск по вариантам имени
        for client in self.clients:
            if search_term in client.search_terms:
                return client
        
        return None