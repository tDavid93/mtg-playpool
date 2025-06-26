from mtgjson_db.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class DeckCards(Base):
    __tablename__ = 'deck_cards'

    deck_id = Column(Integer, ForeignKey('decks.id'), primary_key=True)
    card_id = Column(Integer, ForeignKey('cards.id'), primary_key=True)
    quantity = Column(Integer)

    deck = relationship('Decks', back_populates='deck_cards')
    card = relationship('Cards', back_populates='deck_cards')

class Decks(Base):
    __tablename__ = 'decks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    format = Column(String(255))
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship('User', back_populates='decks')
    deck_cards = relationship('DeckCards', back_populates='deck')

