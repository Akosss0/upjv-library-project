from enum import Enum

class GroupeNom(str, Enum):
    ETUDIANT = "Etudiant"
    PROFESSEUR = "Professeur"
    BIBLIOTHECAIRE = "Bibliothecaire"