from datetime import date
from sqlmodel import SQLModel, Field, Column, Date

class Emprunt(SQLModel, table=True):
    __tablename__: str = "emprunts"

    EMPRUNT_ID: int | None = Field(default=None, primary_key=True)
    EXEMPLAIRE_ID: int = Field(foreign_key="exemplaires.EXEMPLAIRE_ID")
    UTILISATEUR_ID: int
    DATE_EMPRUNT: date = Field(sa_column=Column(Date))
    DATE_RETOUR_PREVU: date = Field(sa_column=Column(Date))
    DATE_RETOUR_EFFECTUE: date | None = Field(default=None, sa_column=Column(Date, nullable=True))
    STATUT_ID: int = Field(foreign_key="statuts.STATUT_ID")