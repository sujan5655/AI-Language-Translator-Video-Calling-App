import os 
from fastapi import Depends,HTTPException,status
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer
from jose import JWTError,jwt
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User

security=HTTPBearer()
JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY")
ALGORITHM=os.getenv("JWT_ALGORITHM","HS256")

# Get Current User
def get_current_user(
    credentials:HTTPAuthorizationCredentials=Depends(security),
    db:Session=Depends(get_db)
)->User:
  token=credentials.credentials
  try:
    payload=jwt.decode(token,JWT_SECRET_KEY,algorithms=[ALGORITHM])
    if payload.get("type")!="access":
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid access token"
      )
    user_id=payload.get("sub")
    if user_id is None:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid access token"
      )
    user_id=int(user_id)
  except (JWTError,ValueError,TypeError):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid or expired access token"
    )
  user=(
    db.query(User).filter(User.id==user_id).first()
  )
  if user is None:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="User not found"
    )
  return user