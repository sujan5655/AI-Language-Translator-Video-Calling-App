from fastapi import APIRouter,Depends
from ..models import User
from .dependencies import get_current_user
router=APIRouter(
  prefix="/users",
  tags=["Users"]
)
@router.get("/me")
async def get_my_profile(
  current_user:User=Depends(get_current_user)
):
  return {
    "message":"Authenticated successfully",
    "user":{
      "id":current_user.id,
      "username":current_user.username,
      "email":current_user.email
    }
  }