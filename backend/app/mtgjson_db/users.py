from mtgjson_db.database import Base


#Fields named "type" are reserved in Python, so we use "card_type" instead
from sqlalchemy import Column, Integer, Float, String, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


import passlib.hash as _hash


class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer,primary_key=True,autoincrement=True)
    username = Column(String(255))
    password = Column(String(255))
    
    