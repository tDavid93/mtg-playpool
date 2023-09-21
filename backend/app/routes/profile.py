from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from mtgjson_db.mtg_models import Cards
from mtgjson_db.users import User

from mtgjson_db.database import get_db

from schemas.user_schemas import SystemUser
from routes.auth.deps import get_current_user

router = APIRouter()

@router.get("/api/profile")
async def get_profile(db: Session = Depends(get_db), user: SystemUser = Depends(get_current_user)):
    print(user)
    user_out = db.query(User).filter(User.username == user.username).first()
    print(user_out)
    return jsonable_encoder(user_out)

