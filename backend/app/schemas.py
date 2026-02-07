from pydantic import BaseModel
from typing import Optional
from datetime import date

# --- Base Schema for config ---
class SchemaBase(BaseModel):
    class Config:
        from_attributes = True

# --- Auth Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    groupe: Optional[str] = None

class Login(BaseModel):
    email: str
    password: str
    
# --- Generic Create Schemas (fields needed for creation) ---

class GroupeCreate(SchemaBase):
    nom: str

class EtatCreate(SchemaBase):
    nom: str

class CategorieCreate(SchemaBase):
    nom: str

class StatutCreate(SchemaBase):
    nom: str

class DepartementCreate(SchemaBase):
    nom: str

class LivreCreate(SchemaBase):
    titre: str
    auteur: str
    categorie_id: int
    resume: Optional[str] = None
    isbn: str
    annee_publication: int
    editeur: str

class ExemplaireCreate(SchemaBase):
    livre_id: int
    etat_id: int
    disponible: bool = True
    date_ajout: date

class UtilisateurCreate(SchemaBase):
    nom: str
    prenom: str
    email: str
    password: str
    departement_id: int
    groupe_id: int

class EmpruntCreate(SchemaBase):
    exemplaire_id: int
    utilisateur_id: int
    date_emprunt: date
    date_retour_prevu: date
    statut_id: int
    # date_retour_effectue is usually null on creation