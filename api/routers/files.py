from fastapi import status, APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import JWTBearer
from folder import Folder


notes = Folder()

router = APIRouter(
    prefix="/files",
    tags=["files"],
)

@router.post("") #, dependencies=[Depends(JWTBearer(role="Administrator"))])
async def add_file(path: str):
    """Add a file."""
    return notes.touch(path)

@router.get("/ls")
async def get_file(path: str=""):
    """Get all files."""
    return notes.ls(path)

@router.get("")
async def get_file(path: str):
    """Get a file content."""
    return notes.cat(path)

@router.put("/{id}") #, dependencies=[Depends(JWTBearer(role="Administrator"))])
async def update_file(path: str, text: str):
    """Update a file."""
    return notes.write(path, text)

@router.delete("", status_code=status.HTTP_204_NO_CONTENT) #, dependencies=[Depends(JWTBearer(role="Administrator"))])
async def delete_file(path: str):
    """Delete a file."""
    return notes.rm(path)
