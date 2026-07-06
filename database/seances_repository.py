from sqlalchemy import select, func
from database.exercices_repository import charger_catalogue
from database.models import Seance, Serie, ExerciceRealise, Exercice

def ajouter_seance(session, date, duree) -> int:
    seance = Seance(date=date, duree=duree)
    session.add(seance)
    session.commit()
    return seance.id_seance

def ajouter_exercice_realise_a_seance(session, id_seance, id_exercice) -> int:
    exercice_realise = ExerciceRealise(id_exercice=id_exercice, id_seance=id_seance)
    session.add(exercice_realise)
    session.commit()
    return exercice_realise.id_exercice_realise

def ajouter_serie(session, numero_serie, poids, reps, est_echauffement, id_exercice_realise) -> int:
    serie = Serie(numero_serie=numero_serie, poids=poids, reps=reps, est_echauffement=est_echauffement, id_exercice_realise=id_exercice_realise)
    session.add(serie)
    session.commit()
    return serie.id_serie

def modifier_date_seance(session, id_seance, nouvelle_date) -> None:
    stmt = select(Seance).where(Seance.id_seance == id_seance)
    seance = session.scalars(stmt).first()
    if seance is not None:
        seance.date = nouvelle_date
        session.commit()


def modifier_duree_seance(session, id_seance, nouvelle_duree) -> None:
    stmt = select(Seance).where(Seance.id_seance == id_seance)
    seance = session.scalars(stmt).first()
    if seance is not None:
        seance.duree = nouvelle_duree
        session.commit()

def modifier_serie(session, id_serie, nouveau_poids, nouvelles_reps, nouvel_est_echauffement) -> None:
    stmt = select(Serie).where(Serie.id_serie == id_serie)
    serie = session.scalars(stmt).first()
    if serie is not None:
        serie.poids = nouveau_poids
        serie.reps = nouvelles_reps
        serie.est_echauffement = nouvel_est_echauffement
        session.commit()

def modifier_poids_serie(session, id_serie, nouveau_poids) -> None:
    stmt = select(Serie).where(Serie.id_serie == id_serie)
    serie = session.scalars(stmt).first()
    if serie is not None:
        serie.poids = nouveau_poids
        session.commit()

def modifier_reps_serie(session, id_serie, nouvelles_reps) -> None:
    stmt = select(Serie).where(Serie.id_serie == id_serie)
    serie = session.scalars(stmt).first()
    if serie is not None:
        serie.reps = nouvelles_reps
        session.commit()

def modifier_echauffement_serie(session, id_serie, nouvel_est_echauffement) -> None:
    stmt = select(Serie).where(Serie.id_serie == id_serie)
    serie = session.scalars(stmt).first()
    if serie is not None:
        serie.est_echauffement = nouvel_est_echauffement
        session.commit()

def supprimer_seance(session, id_seance) -> None:
    stmt = select(Seance).where(Seance.id_seance == id_seance)
    seance = session.scalars(stmt).first()
    if seance is not None:
        session.delete(seance)
        session.commit()

def supprimer_toutes_les_seances(session) -> None:
    seances = session.scalars(select(Seance)).all()
    for seance in seances:
        session.delete(seance)
    session.commit()

def supprimer_exercice_realise(session, id_exercice_realise) -> None:
    stmt = select(ExerciceRealise).where(ExerciceRealise.id_exercice_realise == id_exercice_realise)
    exercice_realise = session.scalars(stmt).first()
    if exercice_realise is not None:
        session.delete(exercice_realise)
        session.commit()

def supprimer_serie(session, id_serie) -> None:
    stmt = select(Serie).where(Serie.id_serie == id_serie)
    serie = session.scalars(stmt).first()
    if serie is not None:
        session.delete(serie)
        session.commit()

def verifier_exercice_realise_existe(session, id_exercice_realise) -> bool:
    stmt = select(ExerciceRealise).where(ExerciceRealise.id_exercice_realise == id_exercice_realise)
    resultat = session.scalars(stmt).first()
    return resultat is not None
    
def verifier_seance_existe(session, id_seance) -> bool:
    stmt = select(Seance).where(Seance.id_seance == id_seance)
    resultat = session.scalars(stmt).first()
    return resultat is not None

def verifier_serie_existe(session, id_serie) -> bool:
    stmt = select(Serie).where(Serie.id_serie == id_serie)
    resultat = session.scalars(stmt).first()
    return resultat is not None

def verifier_exercice_deja_dans_seance(session, id_seance, id_exercice) -> bool:
    stmt = select(ExerciceRealise).where(ExerciceRealise.id_seance == id_seance).where(ExerciceRealise.id_exercice == id_exercice)
    resultat = session.scalars(stmt).first()
    return resultat is not None

def verifier_numero_serie_deja_utilise(session, id_exercice_realise, numero_serie) -> bool:
    stmt = select(Serie).where(Serie.id_exercice_realise == id_exercice_realise).where(Serie.numero_serie == numero_serie)
    resultat = session.scalars(stmt).first()
    return resultat is not None

def verifier_date_seance_existe(session, date) -> bool:
    stmt = select(Seance).where(Seance.date == date)
    resultat = session.scalars(stmt).first()
    return resultat is not None

def lister_seances(session) -> list:
    seances = session.scalars(select(Seance).order_by(Seance.date.desc())).all()
    liste_seances = []
    for seance in seances:
        seances_dict = {"id_seance": seance.id_seance, "date": seance.date, "duree": seance.duree}
        liste_seances.append(seances_dict)
    return liste_seances

def lister_exercices_realises_par_seance(session, id_seance) -> list:
    stmt =(select(Exercice, ExerciceRealise)
           .join(ExerciceRealise, ExerciceRealise.id_exercice == Exercice.id_exercice)
           .where(ExerciceRealise.id_seance == id_seance))
    liste_exercices_realises = []
    for exercice, exercice_realise in session.execute(stmt).all():
        exercices_realises_dict = {"id_exercice_realise": exercice_realise.id_exercice_realise, "id_exercice": exercice.id_exercice, "nom": exercice.nom}
        liste_exercices_realises.append(exercices_realises_dict)
    return liste_exercices_realises

def lister_series_par_exercice_realise(session, id_exercice_realise) -> list:
    stmt = select(Serie).where(Serie.id_exercice_realise == id_exercice_realise).order_by(Serie.numero_serie.asc())
    liste_series = []
    series = session.scalars(stmt).all()
    for serie in series:
        serie_dict = {"id_serie": serie.id_serie, "numero_serie": serie.numero_serie, "poids": serie.poids, "reps": serie.reps, "est_echauffement": serie.est_echauffement}
        liste_series.append(serie_dict)
    return liste_series

def charger_seance_par_date(session, date) -> dict | None:
    stmt = select(Seance).where(Seance.date == date)
    seance = session.scalars(stmt).first()
    if seance is not None:
        return {"id_seance": seance.id_seance, "date": seance.date, "duree": seance.duree}
    else:
        return None

def charger_seance_complete(session, id_seance) -> dict | None:
    stmt = select(Seance).where(Seance.id_seance == id_seance)
    seance = session.scalars(stmt).first()
    if seance is None:
        return None
    catalogue = charger_catalogue(session)
    liste_exercices_realises = []
    exercices_realises = lister_exercices_realises_par_seance(session, id_seance)
    for ligne in exercices_realises:
        liste_series_realises = []
        liste_series = lister_series_par_exercice_realise(session, ligne["id_exercice_realise"])
        for serie in liste_series:
            liste_series_realises.append({"id_serie": serie["id_serie"], "numero_serie": serie["numero_serie"], "poids": serie["poids"], "reps": serie["reps"], "est_echauffement": serie["est_echauffement"]})
        liste_exercices_realises.append({"id_exercice_realise": ligne["id_exercice_realise"], "id_exercice": ligne["id_exercice"], "nom": ligne["nom"], "groupe_musculaire": catalogue[ligne["id_exercice"]]["groupe_musculaire"], "muscles_cibles": catalogue[ligne["id_exercice"]]["muscles_cibles"], "type_materiel": catalogue[ligne["id_exercice"]]["type_materiel"], "series": liste_series_realises})
    seance_complete = {"id_seance": seance.id_seance, "date": seance.date, "duree": seance.duree, "exercices_realises": liste_exercices_realises}
    return seance_complete

def charger_toutes_les_seances_completes(session) -> list:
    stmt = select(Seance)
    seances = session.scalars(stmt).all()
    liste_seances = []
    for seance in seances:
        liste_seances.append(charger_seance_complete(session, seance.id_seance))
    return liste_seances

def enregistrer_seance_complete(session, dict_seance) -> int:
    seance = Seance(date=dict_seance["date"], duree=dict_seance["duree"])
    session.add(seance)
    session.flush()
    id_seance = seance.id_seance
    exercices_realises = dict_seance["exercices_realises"]
    for exo_realise in exercices_realises:
        exercice_realise = ExerciceRealise(id_exercice=exo_realise["id_exercice"], id_seance=id_seance)
        session.add(exercice_realise)
        session.flush()
        id_exercice_realise = exercice_realise.id_exercice_realise
        series = exo_realise["series"]
        for position, ligne in enumerate(series, start=1):
            serie = Serie(numero_serie=position, poids=ligne["poids"], reps=ligne["reps"], est_echauffement=ligne["est_echauffement"], id_exercice_realise=id_exercice_realise)
            session.add(serie)
    session.commit()
    return id_seance

    # cursor = conn.cursor()
    # cursor.execute(
    #     "INSERT INTO seances (date, duree) VALUES (?, ?)", (dict_seance["date"], dict_seance["duree"])
    # )
    # id_seance = cursor.lastrowid
    # exercices_realises = dict_seance["exercices_realises"]
    # for exo_realise in exercices_realises:
    #     cursor.execute(
    #         "INSERT INTO exercices_realises (id_exercice, id_seance) VALUES (?, ?)", (exo_realise["id_exercice"], id_seance)
    #     )
    #     id_exercice_realise = cursor.lastrowid
    #     series = exo_realise["series"]
    #     for position, serie in enumerate(series, start=1):
    #         cursor.execute(
    #             "INSERT INTO series (numero_serie, poids, reps, est_echauffement, id_exercice_realise) VALUES (?, ?, ?, ?, ?)", (position, serie["poids"], serie["reps"], serie["est_echauffement"], id_exercice_realise)
    #         )
    # conn.commit()
    # return id_seance

def prochain_numero(session, id_exercice_realise) -> int:
    stmt = select(func.max(Serie.numero_serie)).where(Serie.id_exercice_realise == id_exercice_realise)
    valeur_max = session.execute(stmt).scalar()
    if valeur_max is None:
        return 1
    return valeur_max + 1
