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