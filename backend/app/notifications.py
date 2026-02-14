"""
Gestion des notifications pour les emprunts
- Emprunts en retard
- Rappels J-30 et J-5 avant la date de retour prévue
"""

from datetime import date, timedelta
from typing import List, Dict, Any
from sqlalchemy.orm import Session, joinedload
from . import models


def get_emprunts_en_retard(db: Session) -> List[Dict[str, Any]]:
    """
    Récupère tous les emprunts en retard (date_retour_prevu dépassée et pas encore rendu)

    Returns:
        Liste de dicts avec les infos de l'emprunt + utilisateur + livre
    """
    today = date.today()

    # Requête : emprunts non rendus (date_retour_effectue == NULL) et en retard
    emprunts = (
        db.query(models.Emprunt)
        .options(
            joinedload(models.Emprunt.utilisateur),
            joinedload(models.Emprunt.exemplaire).joinedload(models.Exemplaire.livre),
        )
        .filter(
            models.Emprunt.date_retour_effectue.is_(None),  # Pas encore rendu
            models.Emprunt.date_retour_prevu < today,  # En retard
        )
        .all()
    )

    result = []
    for emprunt in emprunts:
        jours_retard = (today - emprunt.date_retour_prevu).days

        result.append(
            {
                "emprunt_id": emprunt.emprunt_id,
                "date_emprunt": emprunt.date_emprunt.isoformat(),
                "date_retour_prevu": emprunt.date_retour_prevu.isoformat(),
                "jours_retard": jours_retard,
                "utilisateur": {
                    "id": emprunt.utilisateur.utilisateurs_id,
                    "nom": emprunt.utilisateur.nom,
                    "prenom": emprunt.utilisateur.prenom,
                    "email": emprunt.utilisateur.email,
                },
                "livre": {
                    "id": emprunt.exemplaire.livre.livre_id,
                    "titre": emprunt.exemplaire.livre.titre,
                    "auteur": emprunt.exemplaire.livre.auteur,
                },
                "exemplaire_id": emprunt.exemplaire_id,
            }
        )

    return result


def get_emprunts_rappel_j30(db: Session) -> List[Dict[str, Any]]:
    """
    Récupère les emprunts nécessitant un rappel à J-30
    (date de retour prévue dans 30 jours)

    Returns:
        Liste de dicts avec les infos de l'emprunt + utilisateur + livre
    """
    date_j30 = date.today() + timedelta(days=30)

    emprunts = (
        db.query(models.Emprunt)
        .options(
            joinedload(models.Emprunt.utilisateur),
            joinedload(models.Emprunt.exemplaire).joinedload(models.Exemplaire.livre),
        )
        .filter(
            models.Emprunt.date_retour_effectue.is_(None),  # Pas encore rendu
            models.Emprunt.date_retour_prevu == date_j30,  # Exactement dans 30 jours
        )
        .all()
    )

    result = []
    for emprunt in emprunts:
        result.append(
            {
                "emprunt_id": emprunt.emprunt_id,
                "date_emprunt": emprunt.date_emprunt.isoformat(),
                "date_retour_prevu": emprunt.date_retour_prevu.isoformat(),
                "jours_restants": 30,
                "utilisateur": {
                    "id": emprunt.utilisateur.utilisateurs_id,
                    "nom": emprunt.utilisateur.nom,
                    "prenom": emprunt.utilisateur.prenom,
                    "email": emprunt.utilisateur.email,
                },
                "livre": {
                    "id": emprunt.exemplaire.livre.livre_id,
                    "titre": emprunt.exemplaire.livre.titre,
                    "auteur": emprunt.exemplaire.livre.auteur,
                },
                "exemplaire_id": emprunt.exemplaire_id,
            }
        )

    return result


def get_emprunts_rappel_j5(db: Session) -> List[Dict[str, Any]]:
    """
    Récupère les emprunts nécessitant un rappel à J-5
    (date de retour prévue dans 5 jours)

    Returns:
        Liste de dicts avec les infos de l'emprunt + utilisateur + livre
    """
    date_j5 = date.today() + timedelta(days=5)

    emprunts = (
        db.query(models.Emprunt)
        .options(
            joinedload(models.Emprunt.utilisateur),
            joinedload(models.Emprunt.exemplaire).joinedload(models.Exemplaire.livre),
        )
        .filter(
            models.Emprunt.date_retour_effectue.is_(None),  # Pas encore rendu
            models.Emprunt.date_retour_prevu == date_j5,  # Exactement dans 5 jours
        )
        .all()
    )

    result = []
    for emprunt in emprunts:
        result.append(
            {
                "emprunt_id": emprunt.emprunt_id,
                "date_emprunt": emprunt.date_emprunt.isoformat(),
                "date_retour_prevu": emprunt.date_retour_prevu.isoformat(),
                "jours_restants": 5,
                "utilisateur": {
                    "id": emprunt.utilisateur.utilisateurs_id,
                    "nom": emprunt.utilisateur.nom,
                    "prenom": emprunt.utilisateur.prenom,
                    "email": emprunt.utilisateur.email,
                },
                "livre": {
                    "id": emprunt.exemplaire.livre.livre_id,
                    "titre": emprunt.exemplaire.livre.titre,
                    "auteur": emprunt.exemplaire.livre.auteur,
                },
                "exemplaire_id": emprunt.exemplaire_id,
            }
        )

    return result


def get_tous_les_rappels(db: Session) -> Dict[str, Any]:
    """
    Récupère tous les emprunts nécessitant une notification

    Returns:
        Dict avec les catégories de rappels
    """
    return {
        "en_retard": get_emprunts_en_retard(db),
        "rappel_j30": get_emprunts_rappel_j30(db),
        "rappel_j5": get_emprunts_rappel_j5(db),
    }


def get_notifications_utilisateur(db: Session, utilisateur_id: int) -> Dict[str, Any]:
    """
    Récupère les notifications pour un utilisateur spécifique

    Args:
        utilisateur_id: ID de l'utilisateur

    Returns:
        Dict avec les emprunts en retard et les rappels pour cet utilisateur
    """
    today = date.today()
    date_j30 = today + timedelta(days=30)
    date_j5 = today + timedelta(days=5)

    # Emprunts en retard
    emprunts_retard = (
        db.query(models.Emprunt)
        .options(
            joinedload(models.Emprunt.exemplaire).joinedload(models.Exemplaire.livre)
        )
        .filter(
            models.Emprunt.utilisateur_id == utilisateur_id,
            models.Emprunt.date_retour_effectue.is_(None),
            models.Emprunt.date_retour_prevu < today,
        )
        .all()
    )

    # Rappels J-30
    emprunts_j30 = (
        db.query(models.Emprunt)
        .options(
            joinedload(models.Emprunt.exemplaire).joinedload(models.Exemplaire.livre)
        )
        .filter(
            models.Emprunt.utilisateur_id == utilisateur_id,
            models.Emprunt.date_retour_effectue.is_(None),
            models.Emprunt.date_retour_prevu == date_j30,
        )
        .all()
    )

    # Rappels J-5
    emprunts_j5 = (
        db.query(models.Emprunt)
        .options(
            joinedload(models.Emprunt.exemplaire).joinedload(models.Exemplaire.livre)
        )
        .filter(
            models.Emprunt.utilisateur_id == utilisateur_id,
            models.Emprunt.date_retour_effectue.is_(None),
            models.Emprunt.date_retour_prevu == date_j5,
        )
        .all()
    )

    def format_emprunt(emprunt, jours_info):
        return {
            "emprunt_id": emprunt.emprunt_id,
            "date_emprunt": emprunt.date_emprunt.isoformat(),
            "date_retour_prevu": emprunt.date_retour_prevu.isoformat(),
            **jours_info,
            "livre": {
                "id": emprunt.exemplaire.livre.livre_id,
                "titre": emprunt.exemplaire.livre.titre,
                "auteur": emprunt.exemplaire.livre.auteur,
            },
            "exemplaire_id": emprunt.exemplaire_id,
        }

    return {
        "en_retard": [
            format_emprunt(e, {"jours_retard": (today - e.date_retour_prevu).days})
            for e in emprunts_retard
        ],
        "rappel_j30": [format_emprunt(e, {"jours_restants": 30}) for e in emprunts_j30],
        "rappel_j5": [format_emprunt(e, {"jours_restants": 5}) for e in emprunts_j5],
        "total_notifications": len(emprunts_retard)
        + len(emprunts_j30)
        + len(emprunts_j5),
    }
