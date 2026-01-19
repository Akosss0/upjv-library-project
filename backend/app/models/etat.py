from sqlmodel import SQLModel, Field, Column, Date


class Etat(SQLModel, table=True):
    __tablename__: str = "etats"

    ETAT_ID: int | None = Field(default=None, primary_key=True)
    NOM: str = Field()
