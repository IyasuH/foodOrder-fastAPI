from passlib.context import CryptContext
import time
import secrets
from typing import Dict

import jwt
# from jose import jwt
# from decouple import config


JWT_SECRET = secrets.token_hex(16)
JWR_ALGORITHM = "HS256"
TOKEN_EXPIRE = 30*60 #30 minutes

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hashed(password: str) -> str:
    return password_context.hash(password)

def verify_password(password: str, hashed_pass: str)->bool:
    return password_context.verify(password, hashed_pass)

def token_response(token: str):
    return {
        "access_token": token
    }

def signJWT(admin_id: str) -> Dict[str, str]:
    payload = {
        "admin_id": admin_id,
        "expires": time.time()*TOKEN_EXPIRE
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWR_ALGORITHM)
    return token_response(token)

def decodeJWT(token: str) -> dict:
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=[JWR_ALGORITHM])
        return decode_token if decode_token["expires"]>=time.time() else None
    
    except:
        return {}
