from sqlalchemy import select
from database.models import Exercice, MuscleCibleExercice

def ajouter_exercice(session, id_exercice, nom, groupe_musculaire, type_materiel, muscles_cibles) -> None:
    session.add(Exercice(id_exercice=id_exercice, nom=nom, groupe_musculaire=groupe_musculaire, type_materiel=type_materiel))
    for muscle in muscles_cibles:
        session.add(MuscleCibleExercice(id_exercice=id_exercice, nom_muscle=muscle))
    session.commit()

def charger_catalogue(session) -> dict:
    catalogue = {}
    stmt = (select(Exercice, MuscleCibleExercice)
            .join(MuscleCibleExercice, MuscleCibleExercice.id_exercice == Exercice.id_exercice))
    for exercice, muscle_cible in session.execute(stmt).all():
        id_exercice = exercice.id_exercice
        if id_exercice not in catalogue:
            catalogue[id_exercice] = {"id_exercice": id_exercice, "nom": exercice.nom, "groupe_musculaire": exercice.groupe_musculaire, "type_materiel": exercice.type_materiel, "muscles_cibles": []}
        catalogue[id_exercice]["muscles_cibles"].append(muscle_cible.nom_muscle)
    return catalogue

def verifier_nom_exercice_deja_utilise(session, nom) -> bool:
    stmt = select(Exercice).where(Exercice.nom == nom)
    resultat = session.scalars(stmt).first()
    return resultat is not None

def verifier_id_exercice_existe(session, id_exercice) -> bool:
    stmt = select(Exercice).where(Exercice.id_exercice == id_exercice)
    resultat = session.scalars(stmt).first()
    return resultat is not None