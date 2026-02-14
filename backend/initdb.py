"""
Script d'initialisation de la base de données
Crée les groupes, départements, états, statuts de base
Et un utilisateur administrateur par défaut
"""

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import Groupe, Departement, Etat, Statut, Categorie, Utilisateur
from app.utils import get_password_hash


def init_db():
    """Initialise la base de données avec les données de base"""

    # Créer les tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # --- GROUPES ---
        groupes = ["Bibliothecaire", "Professeur", "Eleve"]
        for nom_groupe in groupes:
            if not db.query(Groupe).filter(Groupe.nom == nom_groupe).first():
                db.add(Groupe(nom=nom_groupe))

        # --- DEPARTEMENTS ---
        departements = [
            "Informatique",
            "Mathématiques",
            "Physique",
            "Chimie",
            "Biologie",
            "Histoire",
            "Géographie",
        ]
        for nom_dept in departements:
            if not db.query(Departement).filter(Departement.nom == nom_dept).first():
                db.add(Departement(nom=nom_dept))

        # --- ETATS ---
        etats = ["Neuf", "Très bon", "Bon", "Acceptable", "Abîmé", "Très abîmé"]
        for nom_etat in etats:
            if not db.query(Etat).filter(Etat.nom == nom_etat).first():
                db.add(Etat(nom=nom_etat))

        # --- STATUTS ---
        statuts = ["En cours", "Rendu à temps", "Rendu en retard", "Perdu"]
        for nom_statut in statuts:
            if not db.query(Statut).filter(Statut.nom == nom_statut).first():
                db.add(Statut(nom=nom_statut))

        # --- CATEGORIES ---
        categories = [
            "Roman",
            "Science-fiction",
            "Fantasy",
            "Policier",
            "Thriller",
            "Histoire",
            "Biographie",
            "Science",
            "Philosophie",
            "Art",
            "Jeunesse",
            "Bande dessinée",
            "Manga",
            "Poésie",
            "Théâtre",
        ]
        for nom_cat in categories:
            if not db.query(Categorie).filter(Categorie.nom == nom_cat).first():
                db.add(Categorie(nom=nom_cat))

        db.commit()

        # --- UTILISATEUR ADMIN ---
        # Créer un bibliothécaire par défaut si aucun n'existe
        admin_email = "admin@library.com"
        if not db.query(Utilisateur).filter(Utilisateur.email == admin_email).first():
            groupe_biblio = (
                db.query(Groupe).filter(Groupe.nom == "Bibliothecaire").first()
            )
            dept_info = (
                db.query(Departement).filter(Departement.nom == "Informatique").first()
            )

            admin = Utilisateur(
                nom="Admin",
                prenom="Bibliothèque",
                email=admin_email,
                password=get_password_hash("admin123"),  # Mot de passe: admin123
                departement_id=dept_info.departement_id,
                groupe_id=groupe_biblio.groupe_id,
            )
            db.add(admin)
            db.commit()
            print(f"✅ Utilisateur admin créé : {admin_email} / admin123")

        print("✅ Base de données initialisée avec succès!")
        print("\n📋 Données créées:")
        print(f"   - {len(groupes)} groupes")
        print(f"   - {len(departements)} départements")
        print(f"   - {len(etats)} états")
        print(f"   - {len(statuts)} statuts")
        print(f"   - {len(categories)} catégories")

    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation : {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("🚀 Initialisation de la base de données...")
    init_db()
