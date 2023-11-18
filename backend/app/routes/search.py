from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from mtgjson_db.mtg_models import Cards

from mtgjson_db.database import  get_db


from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Request

from schemas.user_schemas import SystemUser
from routes.auth.deps import get_current_user
from routes.utils import build_network_card

router = APIRouter()

@router.get("/api/search")
async def search_cards(request : Request,search: str, page: int = 0, db: Session = Depends(get_db), user: SystemUser = Depends(get_current_user)):
    page_limit = 30
    cards = db.query(Cards).filter(Cards.language == 'English').filter(Cards.name.ilike(f'%{search}%',)).order_by(Cards.name).offset(page_limit*page).limit(page_limit).all()
    net_card = []
    for card in cards:
        net_card.append(build_network_card(card, db))
 
    return jsonable_encoder(net_card)

@router.get("/api/cardslist")
async def get_cards_list(page:int = 0, db:Session = Depends(get_db), user: SystemUser = Depends(get_current_user)):
    page_limit = 50
    cards = db.query(Cards).filter(Cards.language == 'English').order_by(Cards.name).offset(page_limit*page).limit(page_limit).all()  
    net_card = []
    for card in cards:
        net_card.append(build_network_card(card,db))
    
    return jsonable_encoder(net_card)
 
