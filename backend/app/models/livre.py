from sqlmodel import SQLModel, Field, Column, Date


class Livre(SQLModel, table=True):
    __tablename__: str = "livres"

    LIVRE_ID: int | None = Field(default=None, primary_key=True)
    TITRE: str = Field()
    AUTEUR: str = Field()
    CATEGORIE_ID: int = Field(foreign_key="categories.CATEGORIE_ID")
    RESUME: str = Field()
    ISBN: str = Field()
    ANNEE_PUBLICATION: int = Field()
    EDITEUR: str = Field()
