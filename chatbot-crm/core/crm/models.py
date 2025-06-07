from pydantic import BaseModel, Field
from typing import Literal

ClientStatus = Literal["new", "loyal", "vip"]

class Client(BaseModel):
    id: str
    name: str
    last_purchase: str
    budget: float = Field(gt=0)
    status: ClientStatus
    
    @property
    def status_emoji(self) -> str:
        return {
            "new": "🆕",
            "loyal": "💎",
            "vip": "👑"
        }[self.status]
    
    @property
    def status_text(self) -> str:
        return {
            "new": "Новый клиент",
            "loyal": "Постоянный клиент",
            "vip": "VIP клиент"
        }[self.status]
    
    @property
    def status_description(self) -> str:
        return {
            "new": "специальные условия для первого заказа",
            "loyal": "персональная скидка 10%",
            "vip": "персональный менеджер и тест-драйв на дом"
        }[self.status]