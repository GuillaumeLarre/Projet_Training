from datetime import datetime

def accord(quantite: int, singulier: str, pluriel: str) -> str:
    if quantite <= 1:
        return singulier
    else:
        return pluriel

def demander_entier_positif(message: str) -> int:
    while True:
        saisie = input(message)
        try:
            valeur = int(saisie)
            if valeur > 0:
                return valeur
            print("La valeur doit être positive")
        except ValueError:
            print("Saisie un nombre entier valide")

def verifier_date(date: str) -> bool:
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False
    
def nb_series_de_travail(exercice_realise) -> int:
    nb_series_de_travail = sum(1 for serie in exercice_realise["series"] if not serie["est_echauffement"])
    return nb_series_de_travail

def volume_total_exercice_realise(exercice_realise) -> float:
    volume_total = 0
    multiplicateur = 2 if exercice_realise["type_materiel"] == "haltères" else 1
    for serie in exercice_realise["series"]:
        poids = serie["poids"]
        reps = serie["reps"]
        if not serie["est_echauffement"]:
            volume_total += (poids * reps * multiplicateur)
    return volume_total