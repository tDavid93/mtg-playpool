import sqlalchemy.orm
from sqlalchemy.orm import Session
from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from settings import (
    ALGORITHM,
    JWT_SECRET
)

from jose import jwt
from pydantic import ValidationError
from schemas.user_schemas import TokenPayload, SystemUser, UserOut
from mtgjson_db.database import get_db
from mtgjson_db.users import User

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/api/login",
    scheme_name="JWT"
)


async def get_current_user(token: str = Depends(reuseable_oauth), db: Session() = Depends(get_db)) -> SystemUser:
    try:
        payload = jwt.decode(
            token, JWT_SECRET, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        print(token_data)
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
     
    user  = db.query(User).filter(User.username == token_data.sub).first()   
    #user: Union[dict[str, Any], None] = db.query(User).filter(token_data.sub == User).first()
    
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    
    return SystemUser(id=user.id, username=user.username, password=user.password)
