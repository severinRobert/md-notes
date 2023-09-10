from fastapi import HTTPException, status, APIRouter, Response, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import JWTBearer


router = APIRouter(
    prefix="/files",
    tags=["files"],
)

@router.post("", dependencies=[Depends(JWTBearer(role="Administrator"))])
async def add_file(file: str, db: Session = Depends(get_db)):
    """Add a file."""
    return None


@router.post("/details", dependencies=[Depends(JWTBearer(role="Administrator"))])
async def add_selection(details: dict[str, int | dict], db: Session = Depends(get_db)):
    return None

@router.get("", response_model=list[str])
async def get_files(db: Session = Depends(get_db)):
    """Get a list of all files."""
    return None


@router.get("/{id}")
async def get_file_id(id: int, db: Session = Depends(get_db)):
    """Get a file by id."""
    return None

@router.put("/{id}", dependencies=[Depends(JWTBearer(role="Administrator"))])
async def update_file(id: int, file: str, db: Session = Depends(get_db)):
    """Update a file."""
    return None

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(JWTBearer(role="Administrator"))])
async def delete_file(id: int, db: Session = Depends(get_db)):
    """Delete a file."""
    return None
