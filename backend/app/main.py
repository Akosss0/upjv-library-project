from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session, joinedload
from typing import List, Type, TypeVar, Optional
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

from . import models, schemas
from .database import engine, get_db, Base

# --- Configuration & Security ---
SECRET_KEY = "YOUR_SUPER_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI()

Base.metadata.create_all(bind=engine)

ModelType = TypeVar("ModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)

# --- Security Utilities ---

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- Auth Dependencies ---

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Fetch user and eager load the group to check permissions
    user = db.query(models.Utilisateur).options(joinedload(models.Utilisateur.groupe)).filter(models.Utilisateur.email == email).first()
    if user is None:
        raise credentials_exception
    return user

class PermissionChecker:
    def __init__(self, allowed_groups: List[str]):
        self.allowed_groups = allowed_groups

    def __call__(self, user: models.Utilisateur = Depends(get_current_user)):
        # If no groups are specified, allow access (or default to stricter logic if preferred)
        if not self.allowed_groups:
            return user
            
        if user.groupe and user.groupe.nom in self.allowed_groups:
            return user
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Operation not permitted for your group"
        )

# --- Routes ---

@app.post("/login", response_model=schemas.Token, tags=["Auth"])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Find user
    user = db.query(models.Utilisateur).filter(models.Utilisateur.email == form_data.username).first()
    
    # Check if user exists and password matches
    # Note: If existing passwords in DB are plain text, this check might fail unless you migrate them.
    # For now, we compare hash.
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create Token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


def create_crud_routes(
    model: Type[ModelType], 
    schema_create: Type[SchemaType], 
    prefix: str, 
    tag: str,
    write_groups: Optional[List[str]] = None
):
    """
    Generates CRUD routes.
    write_groups: List of group names allowed to POST, PUT, PATCH, DELETE. 
                  If None, route is open (or depends on global logic).
    """
    
    # Determine dependencies based on permissions
    write_deps = [Depends(PermissionChecker(write_groups))] if write_groups else []
    
    # Create (POST)
    @app.post(f"/{prefix}/", response_model=schema_create, tags=[tag], dependencies=write_deps)
    def create_item(item: schema_create, db: Session = Depends(get_db)):
        item_data = item.model_dump()
        
        # Security: Hash password if creating a generic user via this route
        if model == models.Utilisateur and "password" in item_data:
            item_data["password"] = get_password_hash(item_data["password"])

        db_item = model(**item_data)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    # Read All (GET)
    @app.get(f"/{prefix}/", response_model=List[schema_create], tags=[tag])
    def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        return db.query(model).offset(skip).limit(limit).all()

    # Read One (GET)
    @app.get(f"/{prefix}/{{item_id}}", response_model=schema_create, tags=[tag])
    def read_item(item_id: int, db: Session = Depends(get_db)):
        pk = model.__mapper__.primary_key[0]
        db_item = db.query(model).filter(pk == item_id).first()
        if db_item is None:
            raise HTTPException(status_code=404, detail=f"{tag} not found")
        return db_item

    # PUT (Full Update - Replaces data, keeps ID)
    @app.put(f"/{prefix}/{{item_id}}", response_model=schema_create, tags=[tag], dependencies=write_deps)
    def update_item_full(item_id: int, item: schema_create, db: Session = Depends(get_db)):
        pk = model.__mapper__.primary_key[0]
        db_item = db.query(model).filter(pk == item_id).first()
        
        if db_item is None:
            raise HTTPException(status_code=404, detail=f"{tag} not found")

        item_data = item.model_dump()
        
        # Handle password hashing on update if it's a user
        if model == models.Utilisateur and "password" in item_data:
            item_data["password"] = get_password_hash(item_data["password"])

        for key, value in item_data.items():
            setattr(db_item, key, value)

        db.commit()
        db.refresh(db_item)
        return db_item

    # PATCH (Partial Update)
    @app.patch(f"/{prefix}/{{item_id}}", response_model=schema_create, tags=[tag], dependencies=write_deps)
    def update_item_partial(item_id: int, item: schema_create, db: Session = Depends(get_db)):
        pk = model.__mapper__.primary_key[0]
        db_item = db.query(model).filter(pk == item_id).first()
        
        if db_item is None:
            raise HTTPException(status_code=404, detail=f"{tag} not found")

        # exclude_unset=True is key for PATCH (only update fields sent)
        item_data = item.model_dump(exclude_unset=True)

        if model == models.Utilisateur and "password" in item_data:
            item_data["password"] = get_password_hash(item_data["password"])

        for key, value in item_data.items():
            setattr(db_item, key, value)

        db.commit()
        db.refresh(db_item)
        return db_item

    # Delete
    @app.delete(f"/{prefix}/{{item_id}}", tags=[tag], dependencies=write_deps)
    def delete_item(item_id: int, db: Session = Depends(get_db)):
        pk = model.__mapper__.primary_key[0]
        db_item = db.query(model).filter(pk == item_id).first()
        if db_item is None:
            raise HTTPException(status_code=404, detail=f"{tag} not found")
        db.delete(db_item)
        db.commit()
        return {"ok": True}

# --- Register Routes ---

# Example: Simple tables (Open access for demo, or restrict as needed)
create_crud_routes(models.Groupe, schemas.GroupeCreate, "groupes", "Groupes", write_groups=["Bibliothecaire"])
create_crud_routes(models.Etat, schemas.EtatCreate, "etats", "Etats", write_groups=["Bibliothecaire"])
create_crud_routes(models.Categorie, schemas.CategorieCreate, "categories", "Categories", write_groups=["Bibliothecaire"])
create_crud_routes(models.Statut, schemas.StatutCreate, "statuts", "Statuts", write_groups=["Bibliothecaire"])
create_crud_routes(models.Departement, schemas.DepartementCreate, "departements", "Departements", write_groups=["Bibliothecaire"])

# Complex Tables
# Books: Only Bibliothecaire can add/edit books. Everyone can read.
create_crud_routes(models.Livre, schemas.LivreCreate, "livres", "Livres", write_groups=["Bibliothecaire"])
create_crud_routes(models.Exemplaire, schemas.ExemplaireCreate, "exemplaires", "Exemplaires", write_groups=["Bibliothecaire"])

# Users: Restricted logic often applies here (e.g., only Admin/Bibliothecaire can delete users)
create_crud_routes(models.Utilisateur, schemas.UtilisateurCreate, "utilisateurs", "Utilisateurs", write_groups=["Bibliothecaire", "Professeur"])

# Emprunts: Bibliothecaire manages loans.
create_crud_routes(models.Emprunt, schemas.EmpruntCreate, "emprunts", "Emprunts", write_groups=["Bibliothecaire"])


@app.get("/")
def read_root():
    return {"message": "Library API is running with MySQL, Auth & RBAC!"}