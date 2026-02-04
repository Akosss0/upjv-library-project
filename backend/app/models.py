from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

# 1. GROUPES
class Groupe(Base):
    __tablename__ = "groupes"
    groupe_id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255))

# 2. ETATS
class Etat(Base):
    __tablename__ = "etats"
    etat_id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255))

# 3. CATEGORIES
class Categorie(Base):
    __tablename__ = "categories"
    categorie_id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255))

# 4. STATUTS
class Statut(Base):
    __tablename__ = "statuts"
    statut_id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255))

# 5. DEPARTEMENTS
class Departement(Base):
    __tablename__ = "departements"
    departement_id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255))

# 6. LIVRES
class Livre(Base):
    __tablename__ = "livres"
    livre_id = Column(Integer, primary_key=True, index=True)
    titre = Column(String(255))
    auteur = Column(String(255))
    categorie_id = Column(Integer, ForeignKey("categories.categorie_id"))
    resume = Column(String(1000))
    isbn = Column(String(50))
    annee_publication = Column(Integer)
    editeur = Column(String(255))

    categorie = relationship("Categorie")

# 7. EXEMPLAIRES
class Exemplaire(Base):
    __tablename__ = "exemplaires"
    exemplaire_id = Column(Integer, primary_key=True, index=True)
    livre_id = Column(Integer, ForeignKey("livres.livre_id"))
    etat_id = Column(Integer, ForeignKey("etats.etat_id"))
    disponible = Column(Boolean, default=True)
    date_ajout = Column(Date)

    livre = relationship("Livre")
    etat = relationship("Etat")

# 8. UTILISATEURS
class Utilisateur(Base):
    __tablename__ = "utilisateurs"
    utilisateurs_id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255))
    prenom = Column(String(255))
    email = Column(String(255), unique=True)
    password = Column(String(255))
    departement_id = Column(Integer, ForeignKey("departements.departement_id"))
    groupe_id = Column(Integer, ForeignKey("groupes.groupe_id"))

    departement = relationship("Departement")
    groupe = relationship("Groupe")

# 9. EMPRUNTS
class Emprunt(Base):
    __tablename__ = "emprunts"
    emprunt_id = Column(Integer, primary_key=True, index=True)
    exemplaire_id = Column(Integer, ForeignKey("exemplaires.exemplaire_id"))
    utilisateur_id = Column(Integer, ForeignKey("utilisateurs.utilisateurs_id"))
    date_emprunt = Column(Date)
    date_retour_prevu = Column(Date)
    date_retour_effectue = Column(Date, nullable=True)
    statut_id = Column(Integer, ForeignKey("statuts.statut_id"))

    exemplaire = relationship("Exemplaire")
    utilisateur = relationship("Utilisateur")
    statut = relationship("Statut")