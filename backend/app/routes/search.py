import routes
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from mtgjson_db.mtg_models import Cards
from mtgjson_db.mtg_models import CardIdentifiers
from mtgjson_db.database import sessionLocal, get_db, engine

from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Request

from schemas.user_schemas import SystemUser
from routes.auth.deps import get_current_user

from routes.search_engine.sentsearch import SentenceSearch
from routes.search_engine.utils import prepare_atomic_df
from fastapi import FastAPI, Depends, HTTPException







# preload the cards from the databese for the search engine


embedder = 'mixedbread-ai/mxbai-embed-large-v1'
reranker = 'cross-encoder/ms-marco-TinyBERT-L-2'

atomic_df = prepare_atomic_df(engine)
search_engine = SentenceSearch(atomic_df, atomic_df['text_repr'], embedder,reranker )
search_engine.load_and_unload_model(embedder)
search_engine.load_reranker(reranker)


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



    
@router.get("/api/transformer_search")
async def transformer_search(query: str = 'magic',filltered_by_collection : bool = True, top_k: int = 1000, page: int = 0, page_size: int = 30, use_reranker: bool = False, db: Session = Depends(get_db)):
    
    print(f"Query: {query}, top_k: {top_k}, page: {page}, page_size: {page_size}, use_reranker: {use_reranker}")
    
    if page < 0 :
        raise HTTPException(status_code=400, detail="Invalid page or page size")

    if query == '' or query is None:
        #return 30 random cards
        query = 'magic'
    try:
        results, query_ttime = search_engine.gradio_search(query, use_reranker, top_k)
        #print(f"Results:\n {'-'*10}\n{results}\n {'-'*10}\nQuery time: {query_ttime}")
        if results is None:
            return {"message": "No matches found."}

         # create network card
        
         
        if use_reranker:
            results = sorted(results, key=lambda x: x['scores'], reverse=True)
            
        start = page * page_size
        end = start + page_size
        paginated_results = results[start:end]
            
        cards = []
        for raw_card in paginated_results:
            cardid = db.query(CardIdentifiers).filter(CardIdentifiers.scryfalloracleid == raw_card['scryfalloracleid']).first()
            if cardid:
                card = db.query(Cards).filter(Cards.uuid == cardid.uuid).first()
                if card:
                    cards.append(card)
        
        net_cards = [build_network_card(card, db) for card in cards]
        
        
         
         
         
        
        return jsonable_encoder(net_cards)
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    


