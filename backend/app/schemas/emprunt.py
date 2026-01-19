from datetime import date
from typing import Optional
from sqlmodel import SQLModel

class EmpruntCreate(SQLModel):
    EXEMPLAIRE_ID: int
    UTILISATEUR_ID: int
    DATE_EMPRUNT: date
    DATE_RETOUR_PREVU: date
    DATE_RETOUR_EFFECTUE: Optional[date] = None
    STATUT_ID: int

class EmpruntRead(EmpruntCreate):
    EMPRUNT_ID: int
