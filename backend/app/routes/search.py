from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from mtgjson_db.mtg_models import Cards
from mtgjson_db.mtg_models import CardIdentifiers
from mtgjson_db.database import sessionLocal, get_db

from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Request

from schemas.user_schemas import SystemUser
from routes.auth.deps import get_current_user

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
 
def build_network_card(card:Cards, db):
    n_card = {
        'name' : card.name,
        'uuid' : card.uuid,
        'img_url': get_image_url(card,db)
    }
    return n_card
 
 
def get_image_url(card:Cards, db:Session = Depends(sessionLocal)):
    """returns the url of the image for the card"""
    try:
        cardid = db.query(CardIdentifiers).filter(CardIdentifiers.uuid == card.uuid).first()
    
    except Exception as e:
        print (e)
        return "https://cards.scryfall.io/art_crop/front/b/d/bd8fa327-dd41-4737-8f19-2cf5eb1f7cdd.jpg"        
    scryfallid = cardid.scryfallid
    fileType = "normal"
    #fileType = "art_crop"
    fileFace = "front"
    
    dir1 = scryfallid[0:1]
    dir2 = scryfallid[1:2]
    fileName = scryfallid
    fileFormat = "jpg"

    img_url = f"https://cards.scryfall.io/{fileType}/{fileFace}/{dir1}/{dir2}/{fileName}.{fileFormat}";
    return img_url