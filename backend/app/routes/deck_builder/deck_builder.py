import sqlalchemy
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from mtgjson_db.mtg_models import Cards
from mtgjson_db.mtg_models import CardIdentifiers
from mtgjson_db.database import sessionLocal, get_db
from mtgjson_db.custom_decks import DeckCards, Decks

from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session
from sqlalchemy.orm import aliased
from fastapi import APIRouter, Depends, Request, HTTPException, status


from schemas.user_schemas import SystemUser
from schemas.deck_shemas import Decks as DeckSchema
from schemas.deck_shemas import DeckCards as DeckCardsSchema

from routes.auth.deps import get_current_user
from routes.utils import build_network_card

from typing import Optional
from mtgjson_db.mtg_models import Cards



router = APIRouter()






@router.post("/api/deck/create")
def create_deck(request: Request, deck:DeckSchema, db: Session = Depends(get_db), user: SystemUser = Depends(get_current_user)):
    try:
        
        db.add(Decks(name=deck.name,
                     description=deck.description,
                     format=deck.format,
                     user_id=user.id))
        db.commit()
        return "Deck created"
    
    except Exception as e:
        print (e)
        return "Error creating deck"
    





@router.post("/api/deck/add_card")
def add_card(request: Request, deck:DeckCardsSchema, db: Session = Depends(get_db), user: SystemUser = Depends(get_current_user)):
    try:
        if not db.query(DeckCards).filter(DeckCards.deck_id == deck.deck_id).filter(DeckCards.card_id == deck.card_id).first():
            
            db.add(DeckCards(deck_id=deck.deck_id,
                             card_id=deck.card_id,
                             quantity=deck.quantity))
            db.commit()
            return "Card added"
        else:
            return "Card already in deck" 
    except Exception as e:
        print (e)
        return "Error adding card"
    




@router.get("/api/deck/get_decks")
def get_decks(db: Session = Depends(get_db), user: SystemUser = Depends(get_current_user)):
    try:
        decks = db.query(Decks).filter(Decks.user_id == user.id).all()
        
        return decks
    
    except Exception as e:
        print ("error: ", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error getting decks"
        )
    
    
    
@router.get("/api/deck/get_deck_cards")
def get_deck_cards(deck_id: int, page:int, search ="" , db: Session = Depends(get_db), user: SystemUser = Depends(get_current_user)):
    page_limit = 30
    try:

        # Perform the join and specify the ON clause
        cards = db.query(DeckCards).filter(DeckCards.deck_id == deck_id).offset(page_limit*page).limit(page_limit).all() 
        print (cards[0].__dict__)

        net_card = []
        for card in cards:
            net_card.append(build_network_card(card, db))

        print (net_card)
        return jsonable_encoder(net_card) 
      
    
    except Exception as e:
        print (e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error getting cards"
        )
         
@router.delete("/api/deck/delete_deck")
def delete_deck(deck_id: int, db: Session = Depends(get_db), user: SystemUser = Depends(get_current_user)):
    try:
        db.query(Decks).filter(Decks.id == deck_id).delete()
        db.commit()
        return "Deck deleted"
    
    except Exception as e:
        print (e)
        return "Error deleting deck"
    
@router.delete("/api/deck/delete_card")
def delete_card(deck_id: int, card_id: str, db: Session = Depends(get_db), user: SystemUser = Depends(get_current_user)):
    try:
        db.query(DeckCards).filter(DeckCards.deck_id == deck_id).filter(DeckCards.card_id == card_id).delete()
        db.commit()
        return "Card deleted"
    
    except Exception as e:
        print (e)
        return "Error deleting card"