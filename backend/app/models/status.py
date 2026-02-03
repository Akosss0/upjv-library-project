from sqlmodel import SQLModel, Field, Column, Date


class Status(SQLModel, table=True):
    __tablename__: str = "status"

    STATUS_ID: int | None = Field(default=None, primary_key=True)
    NOM: str = Field()
