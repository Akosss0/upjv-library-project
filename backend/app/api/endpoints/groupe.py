from backend.app.database import get_db
from sqlmodel import Session
from fastapi import APIRouter, Depends
from app.crud.groupe import create_groupe, read_groupes
from app.schemas.groupe import GroupeCreate, GroupeRead

router = APIRouter()

@router.post("/groupe/", response_model=GroupeRead)
def create(groupe: GroupeCreate, db: Session = Depends(get_db)):
    return create_groupe(db, groupe)

@router.get("/groupe/", response_model=list[GroupeRead])
def read_groupes(db: Session = Depends(get_db)):
    return read_groupes(db)
