from datetime import datetime, timedelta

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
import random


ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
SECRET_KEY = ''.join(random.choice(ALPHABET) for i in range(64))
ALGORITHM = "HS256"



def is_request_owner(request: Request, user_id: int):
    """Check if token is owner."""
    if request.headers.get("authorization"):
        token = request.headers.get("authorization").split(" ")[1]
        payload = get_payload(token)
        if payload is None:
            return None
        return False if not payload else payload['user_id'] == int(user_id)
    return None

def get_payload(jwtoken: str):
    try:
        print("trying to decode")
        payload = jwt.decode(jwtoken, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        return payload
    except Exception as e:
        print(e)
        return None

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True, role: str = None):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.role = role

    # TODO : remove all details for security
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid = False
        try:
            payload = jwt.decode(jwtoken, SECRET_KEY, algorithms=[ALGORITHM])
            if self.role:
                if payload.get("role") != self.role and self.role == "Administrator":
                    payload = None
        except:
            print("Invalid token")
            payload = None
        if payload:
            print("Token is valid !!")
            isTokenValid = True
        return isTokenValid