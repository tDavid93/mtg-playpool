from pydantic import BaseModel
from typing import List
from typing import Optional

class DeckCards(BaseModel):
    deck_id: int
    card_id: str
    quantity: int = 1
    
    
    
class Decks(BaseModel):
    id: Optional[int]
    name: str
    description: Optional[str]
    format: str
    user_id: Optional[int]

