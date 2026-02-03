from sqlmodel import SQLModel, Field, Column, Date


class Departement(SQLModel, table=True):
    __tablename__: str = "departements"

    DEPARTEMENT_ID: int | None = Field(default=None, primary_key=True)
    NOM: str = Field()
