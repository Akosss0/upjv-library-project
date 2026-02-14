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


class TokenData(BaseModel):
    email: Optional[str] = None
    groupe: Optional[str] = None


class Login(BaseModel):
    """Schema pour la connexion"""

    email: EmailStr
    password: str


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


# --- Livre Schemas ---
class LivreCreate(SchemaBase):
    titre: str = Field(..., min_length=1, max_length=255)
    auteur: str = Field(..., min_length=1, max_length=255)
    categorie_id: int
    resume: Optional[str] = Field(None, max_length=1000)
    isbn: str = Field(..., min_length=1, max_length=50)
    annee_publication: int = Field(..., ge=1000, le=9999)
    editeur: str = Field(..., min_length=1, max_length=255)


class LivreUpdate(SchemaBase):
    """Schema pour PATCH - tous les champs optionnels"""

    titre: Optional[str] = Field(None, min_length=1, max_length=255)
    auteur: Optional[str] = Field(None, min_length=1, max_length=255)
    categorie_id: Optional[int] = None
    resume: Optional[str] = Field(None, max_length=1000)
    isbn: Optional[str] = Field(None, min_length=1, max_length=50)
    annee_publication: Optional[int] = Field(None, ge=1000, le=9999)
    editeur: Optional[str] = Field(None, min_length=1, max_length=255)


class LivreResponse(SchemaBase):
    livre_id: int
    titre: str
    auteur: str
    categorie_id: int
    resume: Optional[str]
    isbn: str
    annee_publication: int
    editeur: str


# --- Exemplaire Schemas ---
class ExemplaireCreate(SchemaBase):
    livre_id: int
    etat_id: int
    disponible: bool = True
    date_ajout: date


class ExemplaireUpdate(SchemaBase):
    """Schema pour PATCH - tous les champs optionnels"""

    livre_id: Optional[int] = None
    etat_id: Optional[int] = None
    disponible: Optional[bool] = None
    date_ajout: Optional[date] = None


class ExemplaireResponse(SchemaBase):
    exemplaire_id: int
    livre_id: int
    etat_id: int
    disponible: bool
    date_ajout: date


# --- Utilisateur Schemas ---
class UtilisateurCreate(SchemaBase):
    nom: str = Field(..., min_length=1, max_length=255)
    prenom: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)
    departement_id: int
    groupe_id: int


class UtilisateurUpdate(SchemaBase):
    """Schema pour PATCH - tous les champs optionnels"""

    nom: Optional[str] = Field(None, min_length=1, max_length=255)
    prenom: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6, max_length=100)
    departement_id: Optional[int] = None
    groupe_id: Optional[int] = None


class UtilisateurResponse(SchemaBase):
    """Schema de réponse - sans le mot de passe"""

    utilisateurs_id: int
    nom: str
    prenom: str
    email: str
    departement_id: int
    groupe_id: int


# --- Emprunt Schemas ---
class EmpruntCreate(SchemaBase):
    exemplaire_id: int
    utilisateur_id: int
    date_emprunt: date
    date_retour_prevu: date
    statut_id: int


class EmpruntUpdate(SchemaBase):
    """Schema pour PATCH - tous les champs optionnels"""

    exemplaire_id: Optional[int] = None
    utilisateur_id: Optional[int] = None
    date_emprunt: Optional[date] = None
    date_retour_prevu: Optional[date] = None
    date_retour_effectue: Optional[date] = None
    statut_id: Optional[int] = None


class EmpruntResponse(SchemaBase):
    emprunt_id: int
    exemplaire_id: int
    utilisateur_id: int
    date_emprunt: date
    date_retour_prevu: date
    date_retour_effectue: Optional[date]
    statut_id: int
