
from routes.auth.deps import get_current_user
from fastapi import APIRouter, Depends
from schemas.user_schemas import UserOut, SystemUser


router = APIRouter()

@router.get('/api/me', summary='Get details of currently logged in user', response_model=UserOut)
async def get_me(user: SystemUser = Depends(get_current_user)):
    return user