import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_HOST = os.getenv("DATABASE_HOST")
DB_PORT = os.getenv("DATABASE_PORT")
DB_NAME = os.getenv("DATABASE_NAME")
DB_USER = os.getenv("DATABASE_USER")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD")

DATABASE_URL = (
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}" f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(
    DATABASE_URL,
    echo=True,  # logs SQL (dev only)
    pool_pre_ping=True,  # évite les connexions mortes
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Groupe(SQLModel, table=True):
    id: int | None = Field(default= None, primary_key=True)
    name: str = Field(index=True)

class Emprunt(SQLModel, table=True):
    __tablename__: str = "emprunts"

    EMPRUNT_ID: int | None = Field(default=None, primary_key=True)
    EXEMPLAIRE_ID: int = Field(foreign_key="exemplaires.EXEMPLAIRE_ID")
    UTILISATEUR_ID: int = Field(foreign_key="utilisateurs.UTILISATEUR_ID")
    DATE_EMPRUNT: date = Field(sa_column=Column(Date))
    DATE_RETOUR_PREVU: date = Field(sa_column=Column(Date))
    DATE_RETOUR_EFFECTUE: date | None = Field(default=None, sa_column=Column(Date, nullable=True))
    STATUT_ID: int = Field(foreign_key="statuts.STATUT_ID")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
