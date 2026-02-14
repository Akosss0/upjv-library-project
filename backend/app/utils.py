"""
Fonctions utilitaires pour l'authentification
Centralise le hashage des mots de passe pour garantir la cohérence
"""

from passlib.context import CryptContext

# Configuration unique du contexte de hashage
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie qu'un mot de passe correspond au hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash un mot de passe"""
    return pwd_context.hash(password)
