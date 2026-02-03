from sqlmodel import SQLModel
from app.utils import GroupeNom

class GroupeCreate(SQLModel):
    NOM: GroupeNom

class GroupeRead(GroupeCreate):
    GROUPE_ID: int