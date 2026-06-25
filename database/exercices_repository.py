def ajouter_exercice(conn, id_exercice, nom, groupe_musculaire, type_materiel, muscles_cibles) -> None:
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO exercices (id_exercice, nom, groupe_musculaire, type_materiel) VALUES (?, ?, ?, ?)", (id_exercice, nom, groupe_musculaire, type_materiel)
    )
    lignes_muscles = [(id_exercice, m) for m in muscles_cibles]
    cursor.executemany(
        "INSERT INTO muscles_cibles_exercices (id_exercice, nom_muscle) VALUES (?, ?)", lignes_muscles
    )

def charger_catalogue(conn) -> dict:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM exercices"
    )
    exercices = cursor.fetchall()
    catalogue = {}
    for ligne in exercices:
        liste_muscles_cibles = []
        cursor.execute(
            "SELECT nom_muscle FROM muscles_cibles_exercices WHERE id_exercice = ?", (ligne["id_exercice"],)
        )
        muscles_cibles = cursor.fetchall()
        for muscle in muscles_cibles:
            liste_muscles_cibles.append(muscle["nom_muscle"])
        catalogue[ligne["id_exercice"]] = {"id_exercice": ligne["id_exercice"], "nom": ligne["nom"], "groupe_musculaire": ligne["groupe_musculaire"], "type_materiel": ligne["type_materiel"], "muscles_cibles": liste_muscles_cibles}
    return catalogue

def verifier_id_exercice_existe(conn, id_exercice) -> bool:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id_exercice FROM exercices WHERE id_exercice = ?", (id_exercice,)
    )
    resultat = cursor.fetchone()
    return resultat is not None
    
def verifier_nom_exercice_deja_utilise(conn, nom) -> bool:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT nom FROM exercices WHERE nom = ?", (nom,)
    )
    resultat = cursor.fetchone()
    return resultat is not None
    