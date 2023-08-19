from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
import os

#TODO move to config file
#url = "sqlite:////home/bonefire/proj/react.l/02_fastapi_fullstack/backend/app/mtgjson_db/data/AllPrintings.sqlite"
url = os.environ.get('DATABASE_URL') 

#engine = create_engine(url, connect_args={"check_same_thread": False})
engine = create_engine(url)
#sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()