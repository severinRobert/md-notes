from datetime import timedelta

from schemas import User, Role
from fastapi import HTTPException, status, APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from auth import create_access_token, get_payload, is_request_owner

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/register", response_model=Token)
async def register_user(user: dict[str,str], db: Session = Depends(get_db)):
    """Register a user."""
    user = await User.register(User(**user), db)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email or username already exists.")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    role = await Role.get(user.roles_id, db)
    access_token = create_access_token(
        data={"sub": user.username, "role": role.name, "user_id": user.id}, expires_delta=access_token_expires
    )    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login a user."""
    user = await User.login(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    role = await Role.get(user.roles_id, db)
    access_token = create_access_token(
        data={"sub": form_data.username, "role": role.name, "user_id": user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/{id}/profile")
async def user_profile(id: int, request: Request, db: Session = Depends(get_db)):
    """Get user details for profile."""
    with_details = is_request_owner(request, id)

    profile = {'id': id}
    user = await User.get(id, db)
    profile['username'] = user.username
    if with_details is None:
        return profile
    profile['contact'] = user.contact
    if with_details:
        profile['email'] = user.email
        profile['roles_id'] = user.roles_id
        profile['roles_name'] = (await Role.get(user.roles_id, db)).name
    return profile

@router.put("/{id}")
async def user_profile(id: int, details: dict[str,str|dict], request: Request, db: Session = Depends(get_db)):
    """Update user details."""
    profile = details['profile']
    password = details['password']

    user = await User.login(profile["username"], password, db)
    if not user or not is_request_owner(request, id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return await User.update(user.id, profile, db)

@router.put("/{id}/password")
async def user_profile(id: int, details: dict[str,str], request: Request, db: Session = Depends(get_db)):
    """Update user details."""
    username = details['username']
    new_password = details['new_password']
    old_password = details['old_password']

    user = await User.login(username, old_password, db)
    if not user or not is_request_owner(request, id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return await User.update_password(id, new_password, db)

@router.delete("/{id}")
async def delete_user(id: int, details: dict[str,str], request: Request, db: Session = Depends(get_db)):
    """Delete a user."""
    user = await User.get(id, db)
    if not user or not is_request_owner(request, id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Not authorized to delete user",
            headers={"WWW-Authenticate": "Bearer"}
        )
    password = details['password']
    user = await User.login(user.username, password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Not authorized to delete user",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return await User.delete(id, db)

@router.get("/me")
async def read_users_me(request: Request, db: Session = Depends(get_db)):
    """Get current user."""
    token = request.headers.get("authorization").split(" ")[1]
    payload = get_payload(token)
    response = {
        'id': payload['user_id'],
        'role': payload['role']
    }
    return response

