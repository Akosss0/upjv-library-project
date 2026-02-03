from sqlmodel import SQLModel, Field, Column, Date


class Categorie(SQLModel, table=True):
    __tablename__: str = "categories"

    CATEGORIE_ID: int | None = Field(default=None, primary_key=True)
    NOM: str = Field()
