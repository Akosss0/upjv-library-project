from backend.app.schemas.emprunt import EmpruntCreate
from sqlmodel import Session
from app.models.emprunt import Emprunt

def create_emprunt(db: Session, emprunt: EmpruntCreate):
    db_emprunt = Emprunt.from_orm(emprunt)
    db.add(db_emprunt)
    db.commit()
    return db_emprunt
