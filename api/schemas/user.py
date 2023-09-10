from typing import Optional

from models import Users
from .offer import Offer
from pydantic import BaseModel, constr, EmailStr
from sqlalchemy.orm import Session
import random
import hashlib


class UserInfo(BaseModel):
    username: constr(max_length=40)
    email: EmailStr
    role: constr(max_length=20)

class User(BaseModel):
    id: Optional[int]
    username: constr(max_length=40)
    email: Optional[constr(max_length=150)]
    password: constr(max_length=500)
    salt: Optional[constr(max_length=40)]
    states_id: Optional[int]
    roles_id: Optional[int]

    class Config:
        orm_mode = True

    @classmethod
    async def register(cls, user: 'User', db: Session) -> Optional['user']:
        """
        Add a user to the database.
        """
        # Check if the user already exists by email or name.
        user.email = None if user.email=="" else user.email
        if (user.email is not None and db.query(Users).filter(Users.email == user.email).first()) or db.query(Users).filter(Users.username == user.username).first():
            return 

        # generate salt
        ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        salt = ''.join(random.choice(ALPHABET) for i in range(16))
        # hash the password
        hashed_password = hashlib.sha256(f'{user.password}{salt}'.encode('utf-8')).hexdigest()
        # store the salt and the hashed password in the database
        values = dict(user)
        values.pop('id')
        values['password'] = hashed_password
        values['salt'] = salt
        values['roles_id'] = 2

        db_user = Users(**values)
        db.add(db_user)
        db.commit()
        
        return db_user
    
    @classmethod
    async def login(cls, username, password, db: Session) -> Optional['user']:
        """Check the login of a user."""
        db_user = db.query(Users).filter(Users.username == username).first() or db.query(Users).filter(Users.email == username).first()
        if not db_user:
            return
        # hash the password
        hashed_password = hashlib.sha256(f'{password}{db_user.salt}'.encode('utf-8')).hexdigest()
        if not hashed_password == db_user.password:
            print("Password is not correct")
            return
        return db_user

    @classmethod
    async def get(cls, id: int, db: Session) -> Optional['user']:
        """Get a user from the database from its id."""
        user = db.query(Users).filter(Users.id == id).first()
        return user

    @classmethod
    async def get_all(cls, db: Session) -> list['user']:
        """Return a list of all Users from the database."""
        return db.query(Users).all()

    @classmethod
    async def update(cls, id: int, user: dict, db: Session) -> Optional['user']:
        """Update users of a user."""
        db_user = await cls.get(id, db)
        user['email'] = None if user['email']=="" else user['email']
        if db_user:
            for key, value in user.items():
                setattr(db_user, key, value)
            db.commit()
            db.refresh(db_user)
        return db_user

    @classmethod
    async def update_password(cls, id: int, password: str, db: Session) -> Optional['user']:
        """Update user's password."""
        db_user = await cls.get(id, db)
        hashed_passsword = hashlib.sha256(f'{password}{db_user.salt}'.encode('utf-8')).hexdigest()
        print(hashed_passsword)
        if db_user:
            setattr(db_user, 'password', hashed_passsword)
            db.commit()
            db.refresh(db_user)
        return db_user

    @classmethod
    async def delete(cls, id: int, db: Session) -> Optional['user']:
        """Delete a user and return it. Return None if the user does not exists."""
        user = await cls.get(id, db)
        if not user:
            raise Exception("User does not exist")

        offers = await Offer.get_by_user_id(id, db)
        for offer in offers:
            await Offer.delete(offer.id, db)

        db.delete(user)
        db.commit()
        return user
