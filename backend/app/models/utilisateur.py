from sqlmodel import SQLModel, Field, Column, Date


class Utilisateur(SQLModel, table=True):
    __tablename__: str = "utilisateurs"

    UTILISATEUR_ID: int | None = Field(default=None, primary_key=True)
    NOM: str = Field()
    PRENOM: str = Field()
    EMAIL: str = Field()
    PASSWORD: str = Field()
    DEPARTEMENT_ID: int = Field(foreign_key="departements.DEPARTEMENT_ID")
    GROUPE_ID: int = Field(foreign_key="groupes.GROUPE_ID")
