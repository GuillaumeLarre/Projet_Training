import sqlite3

from database.exercices_repository import charger_catalogue

def ajouter_seance(conn, date, duree) -> int:
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO seances (date, duree) VALUES (?, ?)", (date, duree)
    )
    conn.commit()
    return cursor.lastrowid

def ajouter_exercice_realise_a_seance(conn,id_seance, id_exercice) -> int:
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO exercices_realises (id_exercice, id_seance) VALUES (?, ?)", (id_exercice, id_seance)
    )
    conn.commit()
    return cursor.lastrowid

def ajouter_serie(conn, numero_serie, poids, reps, est_echauffement, id_exercice_realise) -> int:
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO series (numero_serie, poids, reps, est_echauffement, id_exercice_realise) VALUES (?, ?, ?, ?, ?)", (numero_serie, poids, reps, est_echauffement, id_exercice_realise)
    )
    conn.commit()
    return cursor.lastrowid

def lister_seances(conn) -> list[sqlite3.Row]:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id_seance, date, duree FROM seances ORDER BY date DESC"
    )
    resultat = cursor.fetchall()
    return resultat

def charger_seance_par_date(conn, date) -> sqlite3.Row | None:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id_seance, date, duree FROM seances WHERE date = ?", (date,)
    )
    resultat = cursor.fetchone()
    return resultat

def modifier_date_seance(conn, id_seance, nouvelle_date) -> None:
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE seances SET date = ? WHERE id_seance = ?", (nouvelle_date, id_seance)
    )
    conn.commit()

def modifier_duree_seance(conn, id_seance, nouvelle_duree) -> None:
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE seances SET duree = ? WHERE id_seance = ?", (nouvelle_duree, id_seance)
    )
    conn.commit()

def supprimer_seance(conn, id_seance) -> None:
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM seances WHERE id_seance = ?", (id_seance,)
    )
    conn.commit()

def supprimer_toutes_les_seances(conn) -> None:
    cursor = conn.cursor()
    cursor.execute("DELETE FROM seances")
    conn.commit()

def supprimer_exercice_realise(conn, id_exercice_realise) -> None:
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM exercices_realises WHERE id_exercice_realise = ?", (id_exercice_realise,)
    )
    conn.commit()

def modifier_serie(conn, id_serie, nouveau_poids, nouvelles_reps, nouvel_est_echauffement) -> None:
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE series SET poids = ?, reps = ?, est_echauffement = ? WHERE id_serie = ?", (nouveau_poids, nouvelles_reps, nouvel_est_echauffement, id_serie)
    )
    conn.commit()

def supprimer_serie(conn, id_serie) -> None:
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM series WHERE id_serie = ?", (id_serie,)
    )
    conn.commit()

def lister_exercices_realises_par_seance(conn, id_seance) -> list:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT er.id_exercice_realise, er.id_exercice, e.nom FROM exercices_realises er JOIN exercices e ON e.id_exercice = er.id_exercice WHERE er.id_seance = ?", (id_seance,)
    )
    liste_exercice_realise = cursor.fetchall()
    return liste_exercice_realise

def lister_series_par_exercice_realise(conn, id_exercice_realise) -> list:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id_serie, numero_serie, poids, reps, est_echauffement FROM series WHERE id_exercice_realise = ? ORDER BY numero_serie ASC", (id_exercice_realise,)
    )
    liste_series_par_exercice_realise = cursor.fetchall()
    return liste_series_par_exercice_realise

def verifier_exercice_realise_existe(conn, id_exercice_realise) -> bool:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id_exercice_realise FROM exercices_realises WHERE id_exercice_realise = ?", (id_exercice_realise,)
    )
    resultat = cursor.fetchone()
    return resultat is not None
    
def verifier_seance_existe(conn, id_seance) -> bool:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id_seance FROM seances WHERE id_seance = ?", (id_seance,)
    )
    resultat = cursor.fetchone()
    return resultat is not None
    
def verifier_serie_existe(conn, id_serie) -> bool:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id_serie FROM series WHERE id_serie = ?", (id_serie,)
    )
    resultat = cursor.fetchone()
    return resultat is not None

def verifier_exercice_deja_dans_seance(conn, id_seance, id_exercice) -> bool:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id_seance, id_exercice FROM exercices_realises WHERE id_seance = ? AND id_exercice = ?", (id_seance, id_exercice)
    )
    resultat = cursor.fetchone()
    return resultat is not None

def verifier_numero_serie_deja_utilise(conn, id_exercice_realise, numero_serie) -> bool:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id_serie FROM series WHERE id_exercice_realise = ? AND numero_serie = ?", (id_exercice_realise, numero_serie)
    )
    resultat = cursor.fetchone()
    return resultat is not None

def charger_seance_complete(conn, id_seance) -> dict | None:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id_seance, date, duree FROM seances WHERE id_seance = ?", (id_seance,)
    )
    seance = cursor.fetchone()
    if seance is None:
        return None
    catalogue = charger_catalogue(conn)
    liste_exercices_realises = []
    exercices_realises = lister_exercices_realises_par_seance(conn, id_seance)
    for ligne in exercices_realises:
        liste_series_realises = []
        liste_series = lister_series_par_exercice_realise(conn, ligne["id_exercice_realise"])
        for serie in liste_series:
            liste_series_realises.append({"id_serie": serie["id_serie"], "numero_serie": serie["numero_serie"], "poids": serie["poids"], "reps": serie["reps"], "est_echauffement": serie["est_echauffement"]})
        liste_exercices_realises.append({"id_exercice_realise": ligne["id_exercice_realise"], "id_exercice": ligne["id_exercice"], "nom": ligne["nom"], "groupe_musculaire": catalogue[ligne["id_exercice"]]["groupe_musculaire"], "muscles_cibles": catalogue[ligne["id_exercice"]]["muscles_cibles"], "type_materiel": catalogue[ligne["id_exercice"]]["type_materiel"], "series": liste_series_realises})
    seance_complete = {"id_seance": seance["id_seance"], "date": seance["date"], "duree": seance["duree"], "exercices_realises": liste_exercices_realises}
    return seance_complete

def charger_toutes_les_seances_completes(conn) -> list:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id_seance FROM seances"
    )
    liste_seances = []
    resultat = cursor.fetchall()
    for ligne in resultat:
        liste_seances.append(charger_seance_complete(conn, ligne["id_seance"]))
    return liste_seances

def enregistrer_seance_complete(conn, dict_seance) -> int:
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO seances (date, duree) VALUES (?, ?)", (dict_seance["date"], dict_seance["duree"])
    )
    id_seance = cursor.lastrowid
    exercices_realises = dict_seance["exercices_realises"]
    for exo_realise in exercices_realises:
        cursor.execute(
            "INSERT INTO exercices_realises (id_exercice, id_seance) VALUES (?, ?)", (exo_realise["id_exercice"], id_seance)
        )
        id_exercice_realise = cursor.lastrowid
        series = exo_realise["series"]
        for position, serie in enumerate(series, start=1):
            cursor.execute(
                "INSERT INTO series (numero_serie, poids, reps, est_echauffement, id_exercice_realise) VALUES (?, ?, ?, ?, ?)", (position, serie["poids"], serie["reps"], serie["est_echauffement"], id_exercice_realise)
            )
    conn.commit()
    return id_seance

def verifier_date_seance_existe(conn, date) -> bool:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id_seance FROM seances WHERE date = ?", (date,)
    )
    resultat = cursor.fetchone()
    return resultat is not None

def prochain_numero(conn, id_exercice_realise) -> int:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT MAX(numero_serie) FROM series WHERE id_exercice_realise = ?", (id_exercice_realise,)
    )
    resultat = cursor.fetchone()
    valeur_max = resultat[0]
    if valeur_max is None:
        return 1
    return valeur_max + 1

def modifier_poids_serie(conn, id_serie, nouveau_poids) -> None:
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE series SET poids = ? WHERE id_serie = ?", (nouveau_poids, id_serie)
    )
    conn.commit()

def modifier_reps_serie(conn, id_serie, nouvelles_reps) -> None:
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE series SET reps = ? WHERE id_serie = ?", (nouvelles_reps, id_serie)
    )
    conn.commit()

def modifier_echauffement_serie(conn, id_serie, nouvel_est_echauffement) -> None:
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE series SET est_echauffement = ? WHERE id_serie = ?", (nouvel_est_echauffement, id_serie)
    )
    conn.commit()