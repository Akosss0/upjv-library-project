from app.schemas.groupe import GroupeCreate
from sqlmodel import Session, select
from app.models.groupe import Groupe 

def create_groupe(groupe: GroupeCreate, db: Session):
    db_groupe = Groupe(nom=groupe.nom)
    db.add(db_groupe)
    db.commit()
    db.refresh(db_groupe)
    return db_groupe

def read_groupes(db: Session):
    groupes = db.exec(select(Groupe)).all()
    return groupes