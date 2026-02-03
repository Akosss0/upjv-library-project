from sqlmodel import SQLModel, Field, Column, String
from app.utils import GroupeNom

class Groupe(SQLModel, table=True):
    __tablename__:str = "groupes"

    GROUPE_ID: int | None = Field(default=None, primary_key=True)
    NOM: GroupeNom = Field(sa_column=Column(String(20), nullable=False))