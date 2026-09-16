from pwdlib import PasswordHash
from jose import jwt,JWTError
from datetime import datetime,timedelta,timezone
import os
from dotenv import load_dotenv
load_dotenv()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

if not JWT_SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY is missing in .env")

# ============================================================
# PASSWORD HASHING
# ============================================================

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """
    Convert a plain password into a secure password hash.
    """
    return password_hash.hash(password)


def verify_password(
    password: str,
    hashed_password: str,
) -> bool:
    """
    Check whether a plain password matches
    the stored password hash.
    """
    return password_hash.verify(
        password,
        hashed_password,
    )

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7



def create_refresh_token(user_id:int)->str:
    expire=datetime.now(timezone.utc)+timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    )
    payload={
        "sub":str(user_id),
        "type":"refresh",
        "exp":expire
    }
    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=ALGORITHM
    )



def create_access_token(user_id:int)->str:
    expire=datetime.now(timezone.utc)+timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload={
        "sub":str(user_id),
        "type":"access",
        "exp":expire
    }
    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=ALGORITHM
    )




def verify_refresh_token(token:str)->int:
    try:
        payload=jwt.decode(token,JWT_SECRET_KEY,algorithms=[ALGORITHM])
        if payload.get("type")!="refresh":
            raise ValueError("Not a refresh token")
        user_id=payload.get("sub")
        if user_id is None:
            raise ValueError("User ID is missing")
        return int(user_id)
    except(JWTError,ValueError):
        raise ValueError("Invalid or expired refresh token")
            