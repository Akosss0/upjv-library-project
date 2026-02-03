from datetime import date
from sqlmodel import SQLModel, Field, Column, Date


class Exemplaire(SQLModel, table=True):
    __tablename__: str = "exemplaires"

    EXEMPLAIRE_ID: int | None = Field(default=None, primary_key=True)
    LIVRE_ID: int = Field(foreign_key="livres.LIVRE_ID")
    ETAT_ID: int = Field(foreign_key="etats.ETAT_ID")
    DISPONIBLE: bool = Field(default=True)
    DATE_AJOUT: Date = Field(default=date.today(), sa_column=Column(Date))
