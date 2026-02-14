from pydantic import BaseModel, EmailStr, Field
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


class Login(BaseModel):
    """Schema pour la connexion"""

    email: EmailStr
    password: str


class TokenData(BaseModel):
    email: Optional[str] = None
    groupe: Optional[str] = None


# --- Registration Schema ---
class UtilisateurRegister(BaseModel):
    """Schema pour l'inscription d'un nouvel utilisateur"""

    nom: str = Field(..., min_length=1, max_length=255)
    prenom: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(
        ..., min_length=6, max_length=100, description="Minimum 6 caractères"
    )
    departement_id: int
    groupe_id: int


# --- Generic Create Schemas ---


class GroupeCreate(SchemaBase):
    nom: str = Field(..., min_length=1, max_length=255)


class GroupeResponse(SchemaBase):
    groupe_id: int
    nom: str


class EtatCreate(SchemaBase):
    nom: str = Field(..., min_length=1, max_length=255)


class EtatResponse(SchemaBase):
    etat_id: int
    nom: str


class CategorieCreate(SchemaBase):
    nom: str = Field(..., min_length=1, max_length=255)


class CategorieResponse(SchemaBase):
    categorie_id: int
    nom: str


class StatutCreate(SchemaBase):
    nom: str = Field(..., min_length=1, max_length=255)


class StatutResponse(SchemaBase):
    statut_id: int
    nom: str


class DepartementCreate(SchemaBase):
    nom: str = Field(..., min_length=1, max_length=255)


class DepartementResponse(SchemaBase):
    departement_id: int
    nom: str


class LivreCreate(SchemaBase):
    titre: str = Field(..., min_length=1, max_length=255)
    auteur: str = Field(..., min_length=1, max_length=255)
    categorie_id: int
    resume: Optional[str] = Field(None, max_length=1000)
    isbn: str = Field(..., min_length=1, max_length=50)
    annee_publication: int = Field(..., ge=1000, le=9999)
    editeur: str = Field(..., min_length=1, max_length=255)


class LivreResponse(SchemaBase):
    livre_id: int
    titre: str
    auteur: str
    categorie_id: int
    resume: Optional[str]
    isbn: str
    annee_publication: int
    editeur: str


class ExemplaireCreate(SchemaBase):
    livre_id: int
    etat_id: int
    disponible: bool = True
    date_ajout: date


class ExemplaireResponse(SchemaBase):
    exemplaire_id: int
    livre_id: int
    etat_id: int
    disponible: bool
    date_ajout: date


class UtilisateurCreate(SchemaBase):
    nom: str = Field(..., min_length=1, max_length=255)
    prenom: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)
    departement_id: int
    groupe_id: int


class UtilisateurResponse(SchemaBase):
    """Schema de réponse - sans le mot de passe"""

    utilisateurs_id: int
    nom: str
    prenom: str
    email: str
    departement_id: int
    groupe_id: int


class EmpruntCreate(SchemaBase):
    exemplaire_id: int
    utilisateur_id: int
    date_emprunt: date
    date_retour_prevu: date
    statut_id: int


class EmpruntResponse(SchemaBase):
    emprunt_id: int
    exemplaire_id: int
    utilisateur_id: int
    date_emprunt: date
    date_retour_prevu: date
    date_retour_effectue: Optional[date]
    statut_id: int
