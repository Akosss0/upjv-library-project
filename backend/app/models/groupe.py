from sqlmodel import SQLModel, Field, Column, Date

class Groupe(SQLModel, table=True):
    __tablename__:str = "groupes"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field()