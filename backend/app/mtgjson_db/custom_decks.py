from mtgjson_db.database import Base


#Fields named "type" are reserved in Python, so we use "card_type" instead
from sqlalchemy import Column, Integer, Float, String, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

from mtgjson_db.mtg_models import Cards
from mtgjson_db.users import User

import passlib.hash as _hash


class Decks(Base):
    __tablename__ = 'decks'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    format = Column(String(255))
    
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    
    user = relationship("User")

class DeckCards(Base):
    __tablename__ = 'deck_cards'
    
    deck_id = Column(Integer, ForeignKey(Decks.id), primary_key=True)
    card_id = Column(String(36), ForeignKey(Cards.uuid), nullable=False)
    quantity = Column(Integer)
 
       
    deck = relationship("Decks")
    card = relationship("Cards")
