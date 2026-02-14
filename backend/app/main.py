from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session, joinedload
from typing import List, Type, TypeVar, Optional
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os

from . import models, schemas
from .database import engine, get_db, Base
from .utils import verify_password, get_password_hash

# --- Configuration & Security ---
SECRET_KEY = os.getenv("SECRET_KEY", "YOUR_SUPER_SECRET_KEY_CHANGE_IN_PRODUCTION")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()

app = FastAPI(
    title="Library Management API",
    description="API de gestion de bibliothèque avec authentification JWT",
    version="1.0.0",
)

Base.metadata.create_all(bind=engine)

ModelType = TypeVar("ModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)

# --- Security Utilities ---


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


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Fetch user and eager load the group to check permissions
    user = (
        db.query(models.Utilisateur)
        .options(joinedload(models.Utilisateur.groupe))
        .filter(models.Utilisateur.email == email)
        .first()
    )
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
            detail="Operation not permitted for your group",
        )


# --- Auth Routes ---


@app.post(
    "/register",
    response_model=schemas.UtilisateurResponse,
    tags=["Auth"],
    status_code=status.HTTP_201_CREATED,
)
def register(user_data: schemas.UtilisateurRegister, db: Session = Depends(get_db)):
    """
    Inscription d'un nouvel utilisateur.
    Email doit être unique.
    Le mot de passe est automatiquement hashé.
    """
    # Vérifier si l'email existe déjà
    existing_user = (
        db.query(models.Utilisateur)
        .filter(models.Utilisateur.email == user_data.email)
        .first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # Vérifier que le département existe
    departement = (
        db.query(models.Departement)
        .filter(models.Departement.departement_id == user_data.departement_id)
        .first()
    )
    if not departement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Departement not found"
        )

    # Vérifier que le groupe existe
    groupe = (
        db.query(models.Groupe)
        .filter(models.Groupe.groupe_id == user_data.groupe_id)
        .first()
    )
    if not groupe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Groupe not found"
        )

    # Créer le nouvel utilisateur avec mot de passe hashé
    new_user = models.Utilisateur(
        nom=user_data.nom,
        prenom=user_data.prenom,
        email=user_data.email,
        password=get_password_hash(user_data.password),
        departement_id=user_data.departement_id,
        groupe_id=user_data.groupe_id,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.post("/login", response_model=schemas.Token, tags=["Auth"])
def login_for_access_token(login_data: schemas.Login, db: Session = Depends(get_db)):
    """
    Connexion avec email et mot de passe.
    Retourne un token JWT Bearer.
    """
    # Find user
    user = (
        db.query(models.Utilisateur)
        .filter(models.Utilisateur.email == login_data.email)
        .first()
    )

    # Check if user exists and password matches
    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create Token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/me", response_model=schemas.UtilisateurResponse, tags=["Auth"])
def get_current_user_info(current_user: models.Utilisateur = Depends(get_current_user)):
    """
    Récupère les informations de l'utilisateur connecté.
    """
    return current_user


# --- CRUD Generator ---


def create_crud_routes(
    model: Type[ModelType],
    schema_create: Type[SchemaType],
    schema_response: Type[SchemaType],
    prefix: str,
    tag: str,
    write_groups: Optional[List[str]] = None,
    schema_update: Optional[Type[SchemaType]] = None,  # Nouveau paramètre
):
    """
    Generates CRUD routes.
    write_groups: List of group names allowed to POST, PUT, PATCH, DELETE.
    schema_update: Optional schema for PATCH with optional fields
    """

    # Determine dependencies based on permissions
    write_deps = [Depends(PermissionChecker(write_groups))] if write_groups else []

    # Utiliser schema_update pour PATCH si fourni, sinon utiliser schema_create
    patch_schema = schema_update if schema_update else schema_create

    # Create (POST)
    @app.post(
        f"/{prefix}/",
        response_model=schema_response,
        tags=[tag],
        dependencies=write_deps,
        status_code=status.HTTP_201_CREATED,
    )
    def create_item(item: schema_create, db: Session = Depends(get_db)):
        item_data = item.model_dump()

        # Security: Hash password if creating a generic user via this route
        if model == models.Utilisateur and "password" in item_data:
            # Vérifier email unique
            if (
                db.query(models.Utilisateur)
                .filter(models.Utilisateur.email == item_data["email"])
                .first()
            ):
                raise HTTPException(status_code=400, detail="Email already registered")
            item_data["password"] = get_password_hash(item_data["password"])

        db_item = model(**item_data)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    # Read All (GET)
    @app.get(f"/{prefix}/", response_model=List[schema_response], tags=[tag])
    def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        return db.query(model).offset(skip).limit(limit).all()

    # Read One (GET)
    @app.get(f"/{prefix}/{{item_id}}", response_model=schema_response, tags=[tag])
    def read_item(item_id: int, db: Session = Depends(get_db)):
        pk = model.__mapper__.primary_key[0]
        db_item = db.query(model).filter(pk == item_id).first()
        if db_item is None:
            raise HTTPException(status_code=404, detail=f"{tag} not found")
        return db_item

    # PUT (Full Update - Replaces data, keeps ID)
    @app.put(
        f"/{prefix}/{{item_id}}",
        response_model=schema_response,
        tags=[tag],
        dependencies=write_deps,
    )
    def update_item_full(
        item_id: int, item: schema_create, db: Session = Depends(get_db)
    ):
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
    @app.patch(
        f"/{prefix}/{{item_id}}",
        response_model=schema_response,
        tags=[tag],
        dependencies=write_deps,
    )
    def update_item_partial(
        item_id: int, item: patch_schema, db: Session = Depends(get_db)
    ):
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
    @app.delete(
        f"/{prefix}/{{item_id}}",
        tags=[tag],
        dependencies=write_deps,
        status_code=status.HTTP_204_NO_CONTENT,
    )
    def delete_item(item_id: int, db: Session = Depends(get_db)):
        pk = model.__mapper__.primary_key[0]
        db_item = db.query(model).filter(pk == item_id).first()
        if db_item is None:
            raise HTTPException(status_code=404, detail=f"{tag} not found")
        db.delete(db_item)
        db.commit()
        return None


# --- Register Routes ---

# Simple tables (Only Bibliothecaire can modify)
create_crud_routes(
    models.Groupe,
    schemas.GroupeCreate,
    schemas.GroupeResponse,
    "groupes",
    "Groupes",
    write_groups=["Bibliothecaire"],
)
create_crud_routes(
    models.Etat,
    schemas.EtatCreate,
    schemas.EtatResponse,
    "etats",
    "Etats",
    write_groups=["Bibliothecaire"],
)
create_crud_routes(
    models.Categorie,
    schemas.CategorieCreate,
    schemas.CategorieResponse,
    "categories",
    "Categories",
    write_groups=["Bibliothecaire"],
)
create_crud_routes(
    models.Statut,
    schemas.StatutCreate,
    schemas.StatutResponse,
    "statuts",
    "Statuts",
    write_groups=["Bibliothecaire"],
)
create_crud_routes(
    models.Departement,
    schemas.DepartementCreate,
    schemas.DepartementResponse,
    "departements",
    "Departements",
    write_groups=["Bibliothecaire"],
)

# Books: Only Bibliothecaire can add/edit books - AVEC SCHEMA UPDATE
create_crud_routes(
    models.Livre,
    schemas.LivreCreate,
    schemas.LivreResponse,
    "livres",
    "Livres",
    write_groups=["Bibliothecaire"],
    schema_update=schemas.LivreUpdate,  # Nouveau !
)

create_crud_routes(
    models.Exemplaire,
    schemas.ExemplaireCreate,
    schemas.ExemplaireResponse,
    "exemplaires",
    "Exemplaires",
    write_groups=["Bibliothecaire"],
    schema_update=schemas.ExemplaireUpdate,  # Nouveau !
)

# Users: Bibliothecaire and Professeur can manage - AVEC SCHEMA UPDATE
create_crud_routes(
    models.Utilisateur,
    schemas.UtilisateurCreate,
    schemas.UtilisateurResponse,
    "utilisateurs",
    "Utilisateurs",
    write_groups=["Bibliothecaire", "Professeur"],
    schema_update=schemas.UtilisateurUpdate,  # Nouveau !
)

# Loans: Bibliothecaire manages loans - AVEC SCHEMA UPDATE
create_crud_routes(
    models.Emprunt,
    schemas.EmpruntCreate,
    schemas.EmpruntResponse,
    "emprunts",
    "Emprunts",
    write_groups=["Bibliothecaire"],
    schema_update=schemas.EmpruntUpdate,  # Nouveau !
)


@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": "Library API is running with MySQL, Auth & RBAC!",
        "version": "1.0.0",
        "docs": "/docs",
    }
