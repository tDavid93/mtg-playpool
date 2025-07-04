from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware


from mtgjson_db.database import engine, sessionLocal
from mtgjson_db.mtg_models import *
from mtgjson_db.custom_decks import Decks, DeckCards  
from mtgjson_db.users import User
from routes import search
from routes.auth import register
from routes.auth import login
from routes.auth import me
from routes import profile

Base.metadata.create_all(bind=engine)
##
app = FastAPI(
            docs_url='/api/docs',
            redoc_url='/api/redoc',
            openapi_url='/api/openapi.json'
)

app.include_router(search.router)
app.include_router(register.router)
app.include_router(login.router)
app.include_router(me.router)
app.include_router(profile.router)

# Cross Origin Resource Sharing (CORS) adresses
origins = [
    "nginx"
    "http://nginx",
    "http://localhost:8050",
    "localhost:8050",
    "http://localhost:3000",
    "0.0.0.0:3000",   
    "http://127.0.0.1:8050",
    "http://127.0.0.1:3000",
    
]

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
