from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Type, TypeVar
from pydantic import BaseModel

from . import models, schemas
from .database import engine, get_db, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

ModelType = TypeVar("ModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)

def create_crud_routes(
    model: Type[ModelType], 
    schema_create: Type[SchemaType], 
    prefix: str, 
    tag: str
):
    # Create
    @app.post(f"/{prefix}/", response_model=schema_create, tags=[tag])
    def create_item(item: schema_create, db: Session = Depends(get_db)):
        db_item = model(**item.model_dump())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    # Read All
    @app.get(f"/{prefix}/", response_model=List[schema_create], tags=[tag])
    def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        return db.query(model).offset(skip).limit(limit).all()

    # Read One
    @app.get(f"/{prefix}/{{item_id}}", response_model=schema_create, tags=[tag])
    def read_item(item_id: int, db: Session = Depends(get_db)):
        # Assumes primary key is the first column or named specifically. 
        # For simplicity in this factory, we fetch by the primary key generic search
        pk = model.__mapper__.primary_key[0]
        db_item = db.query(model).filter(pk == item_id).first()
        if db_item is None:
            raise HTTPException(status_code=404, detail=f"{tag} not found")
        return db_item

    # Delete
    @app.delete(f"/{prefix}/{{item_id}}", tags=[tag])
    def delete_item(item_id: int, db: Session = Depends(get_db)):
        pk = model.__mapper__.primary_key[0]
        db_item = db.query(model).filter(pk == item_id).first()
        if db_item is None:
            raise HTTPException(status_code=404, detail=f"{tag} not found")
        db.delete(db_item)
        db.commit()
        return {"ok": True}

# --- Register Routes for ALL Tables ---

# Simple Tables
create_crud_routes(models.Groupe, schemas.GroupeCreate, "groupes", "Groupes")
create_crud_routes(models.Etat, schemas.EtatCreate, "etats", "Etats")
create_crud_routes(models.Categorie, schemas.CategorieCreate, "categories", "Categories")
create_crud_routes(models.Statut, schemas.StatutCreate, "statuts", "Statuts")
create_crud_routes(models.Departement, schemas.DepartementCreate, "departements", "Departements")

# Complex Tables
create_crud_routes(models.Livre, schemas.LivreCreate, "livres", "Livres")
create_crud_routes(models.Exemplaire, schemas.ExemplaireCreate, "exemplaires", "Exemplaires")
create_crud_routes(models.Utilisateur, schemas.UtilisateurCreate, "utilisateurs", "Utilisateurs")
create_crud_routes(models.Emprunt, schemas.EmpruntCreate, "emprunts", "Emprunts")

@app.get("/")
def read_root():
    return {"message": "Library API is running with MySQL!"}