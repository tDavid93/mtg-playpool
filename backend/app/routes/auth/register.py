from fastapi import FastAPI, status, HTTPException, Depends
import fastapi.params
from fastapi.responses import RedirectResponse
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from schemas.user_schemas import UserOut, UserAuth
from mtgjson_db.database import get_db
from mtgjson_db.users import User
from routes.auth.utils import get_hashed_password
import sqlalchemy.orm
from uuid import uuid4



router = APIRouter()

@router.post('/api/signup', summary="Create new user", response_model=UserOut)
async def create_user(data: UserAuth, db: Session = Depends(get_db)):
    # querying database to check if user already exist
    user = db.query(User).filter(User.username == data.username).first()
    if user is not None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    print(user)
    user = User(username=data.username, password=get_hashed_password(data.password))
    #Add user to database
    # 
    db.add(user)
    db.commit()
    
    
    return UserOut(id=user.id, username=user.username)