from fastapi import FastAPI, Request
from fastapi.params import Depends
from fastapi.middleware.cors import CORSMiddleware


from fastapi.encoders import jsonable_encoder


from mtgjson_db.database import engine, sessionLocal
from mtgjson_db.mtg_models import *
from sqlalchemy.orm import Session

import json

Base.metadata.create_all(bind=engine)

app = FastAPI()


origins = [
    "nginx"
    "http://nginx",
    "http://localhost:8080",
    "localhost:8080",
    "http://localhost:3000",
    "0.0.0.0:3000"
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def index():
    
    return {"message": "hello"}


@app.get("/cards")
async def get_cards(page:int = 0, db:Session = Depends(get_db)):
    page_limit = 5
    cards = db.query(Cards).limit(page_limit).all()  
    net_card = {}
    for card in cards:
        net_card[card.name] = build_network_card(card, db)
    
    return json.dumps(net_card)

@app.get("/api/cardslist")
async def get_cards_list(page:int = 0, db:Session = Depends(get_db)):
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
 
 
def get_image_url(card:Cards, db:Session = Depends(get_db)):
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