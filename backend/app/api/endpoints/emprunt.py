from backend.app.database import get_db
from sqlmodel import Session
from fastapi import APIRouter, Depends
from app.crud.emprunt import create_emprunt
from app.schemas.emprunt import EmpruntCreate, EmpruntRead

router = APIRouter()

@router.post("/emprunt/", response_model=EmpruntRead)
def create(emprunt: EmpruntCreate, db: Session = Depends(get_db)):
    return create_emprunt(db, emprunt)
