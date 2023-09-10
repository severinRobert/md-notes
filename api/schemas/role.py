from typing import Optional

from models import Roles
from pydantic import BaseModel, constr
from sqlalchemy.orm import Session


class Role(BaseModel):
    id: Optional[int]
    name: constr(max_length=20)
    description: Optional[constr(max_length=255)]

    class Config:
        orm_mode = True

    @classmethod
    async def get(cls, id: int, db: Session) -> Optional['role']:
        """Get a role from the database from its id."""
        role = db.query(Roles).filter(Roles.id == id).first()
        return role

    @classmethod
    async def get_all(cls, db: Session) -> list['role']:
        """Return a list of all Roles from the database."""
        return db.query(Roles).all()
