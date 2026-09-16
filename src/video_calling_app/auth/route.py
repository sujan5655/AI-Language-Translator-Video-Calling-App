from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from .config import hash_password, verify_password,create_access_token,create_refresh_token,verify_refresh_token
from ..database import get_db
from ..models import User


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# ============================================================
# REGISTER SCHEMA
# ============================================================

class RegisterRequest(BaseModel):

    username: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
  email:EmailStr
  password:str


class RefreshRequest(BaseModel):
    refresh_token:str


# ============================================================
# REGISTER
# ============================================================

@router.post("/register")
async def register(
    data: RegisterRequest,
    db: Session = Depends(get_db),
):

    # --------------------------------------------------------
    # Check username
    # --------------------------------------------------------

    existing_username = (
        db.query(User)
        .filter(User.username == data.username)
        .first()
    )

    if existing_username:

        raise HTTPException(
            status_code=400,
            detail="Username already exists",
        )


    # --------------------------------------------------------
    # Check email
    # --------------------------------------------------------

    existing_email = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )

    if existing_email:

        raise HTTPException(
            status_code=400,
            detail="Email already exists",
        )


    # --------------------------------------------------------
    # Hash password
    # --------------------------------------------------------

    password_hash_value = hash_password(
        data.password
    )


    # --------------------------------------------------------
    # Create user
    # --------------------------------------------------------

    user = User(
        username=data.username,
        email=data.email,
        password_hash=password_hash_value,
    )

    db.add(user)

    db.commit()

    db.refresh(user)


    # --------------------------------------------------------
    # Response
    # --------------------------------------------------------

    return {
        "message": "User registered successfully",

        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        },
    }



@router.post("/login")
async def login(data:LoginRequest,db:Session=Depends(get_db),):
    user=(db.query(User).filter(User.email==data.email).first())
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    password_valid=verify_password(data.password,user.password_hash)

    if not password_valid:
      raise HTTPException(
        status_code=401,
        detail="Invalid email or password"
      )
    access_token=create_access_token(user.id)
    refresh_token=create_refresh_token(user.id)
    return {
        "message":"Login Successfull",
        "access_token":access_token,
        "refresh_token":refresh_token,
        "user":{
            "id":user.id,
            "username":user.username,
            "email":user.email
        }
    }



@router.post("/refresh")
async def refresh_access_token(
    data:RefreshRequest,
    db:Session=Depends(get_db)
):
    try:
        user_id=verify_refresh_token(data.refresh_token)
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token"
                            )
    user=(
        db.query(User).filter(User.id==user_id).first()
    )
    if not user:
        raise HTTPException(status_code=401,detail="User not found")
    new_access_token=create_access_token(user.id)
    return {
        "access_token":new_access_token,
        "token_type":"bearer"
    }

    