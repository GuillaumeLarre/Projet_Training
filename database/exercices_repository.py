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
    catalogue = {}
    cursor.execute(
        "SELECT e.id_exercice, e.nom, e.groupe_musculaire, e.type_materiel, m.nom_muscle FROM exercices e JOIN muscles_cibles_exercices m ON m.id_exercice = e.id_exercice"
    )
    exercices = cursor.fetchall()
    for ligne in exercices:
        id_ex = ligne["id_exercice"]
        if id_ex not in catalogue:
            catalogue[id_ex] = {"id_exercice": id_ex, "nom": ligne["nom"], "groupe_musculaire": ligne["groupe_musculaire"], "type_materiel": ligne["type_materiel"], "muscles_cibles": []}
        catalogue[id_ex]["muscles_cibles"].append(ligne["nom_muscle"])
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
    