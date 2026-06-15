import sys
from models.CarnetEntrainement import CarnetEntrainement
from models.Seance import Seance
from models.ExerciceRealise import ExerciceRealise
from models.Serie import Serie

def ajouter_si_absent(carnet, seance):
    for s in carnet.seances:
        if s.date == seance.date:
            print(f"⚠️  Séance déjà existante pour le {seance.date}, ignorée.")
            return
    carnet.ajouter_seance(seance)


def ajouter_seances():

    carnet = CarnetEntrainement.charger("carnet.json")
    
    if not carnet.exercices:
        print("⚠️  Le catalogue est vide. Lance d'abord seed.py.")
        sys.exit()

    

    seance = Seance("2026-06-08", 105)

    exo = ExerciceRealise(carnet.exercices["DC01"])
    exo.ajouter_serie(Serie(30, 13))
    exo.ajouter_serie(Serie(30, 10))
    exo.ajouter_serie(Serie(30, 9))
    seance.ajouter_exercice(exo)

    exo = ExerciceRealise(carnet.exercices["DI01"])
    exo.ajouter_serie(Serie(24, 13))
    exo.ajouter_serie(Serie(24, 12))
    exo.ajouter_serie(Serie(24, 10))
    seance.ajouter_exercice(exo)

    exo = ExerciceRealise(carnet.exercices["EP01"])
    exo.ajouter_serie(Serie(14, 15))
    exo.ajouter_serie(Serie(14, 13))
    exo.ajouter_serie(Serie(14, 10))
    seance.ajouter_exercice(exo)

    exo = ExerciceRealise(carnet.exercices["CP01"])
    exo.ajouter_serie(Serie(51, 15))
    exo.ajouter_serie(Serie(51, 13))
    exo.ajouter_serie(Serie(51, 11))
    seance.ajouter_exercice(exo)

    exo = ExerciceRealise(carnet.exercices["CU01"])
    exo.ajouter_serie(Serie(20, 13))
    exo.ajouter_serie(Serie(20, 12))
    exo.ajouter_serie(Serie(20, 10))
    seance.ajouter_exercice(exo)

    exo = ExerciceRealise(carnet.exercices["EL01"])
    exo.ajouter_serie(Serie(9, 20))
    exo.ajouter_serie(Serie(9, 18))
    exo.ajouter_serie(Serie(11, 15))
    exo.ajouter_serie(Serie(9, 18))
    seance.ajouter_exercice(exo)

    exo = ExerciceRealise(carnet.exercices["EA01"])
    exo.ajouter_serie(Serie(9, 20))
    exo.ajouter_serie(Serie(9, 18))
    exo.ajouter_serie(Serie(9, 16))
    seance.ajouter_exercice(exo)

    ajouter_si_absent(carnet, seance)

    seance = Seance("2026-06-09", 105)

    exo = ExerciceRealise(carnet.exercices["LE01"])
    exo.ajouter_serie(Serie(107, 13))
    exo.ajouter_serie(Serie(107, 11))
    exo.ajouter_serie(Serie(107, 10))
    seance.ajouter_exercice(exo)

    exo = ExerciceRealise(carnet.exercices["HS01"])
    exo.ajouter_serie(Serie(90, 13))
    exo.ajouter_serie(Serie(90, 11))
    exo.ajouter_serie(Serie(90, 10))
    seance.ajouter_exercice(exo)

    exo = ExerciceRealise(carnet.exercices["PR01"])
    exo.ajouter_serie(Serie(120, 13))
    exo.ajouter_serie(Serie(140, 12))
    exo.ajouter_serie(Serie(140, 10))
    seance.ajouter_exercice(exo)

    exo = ExerciceRealise(carnet.exercices["LC01"])
    exo.ajouter_serie(Serie(50, 15))
    exo.ajouter_serie(Serie(50, 13))
    exo.ajouter_serie(Serie(50, 11))
    seance.ajouter_exercice(exo)

    exo = ExerciceRealise(carnet.exercices["LA01"])
    exo.ajouter_serie(Serie(52, 13))
    exo.ajouter_serie(Serie(59, 12))
    exo.ajouter_serie(Serie(59, 10))
    seance.ajouter_exercice(exo)

    exo = ExerciceRealise(carnet.exercices["AD01"])
    exo.ajouter_serie(Serie(45, 20))
    exo.ajouter_serie(Serie(52, 13))
    exo.ajouter_serie(Serie(52, 11))
    seance.ajouter_exercice(exo)

    ajouter_si_absent(carnet, seance)

    seance = Seance("2026-06-10", 105)

    exo = ExerciceRealise(carnet.exercices["RV01"])
    exo.ajouter_serie(Serie(73, 12))
    exo.ajouter_serie(Serie(73, 11))
    exo.ajouter_serie(Serie(73, 10))
    seance.ajouter_exercice(exo)

    exo = ExerciceRealise(carnet.exercices["TV01"])
    exo.ajouter_serie(Serie(86, 13))
    exo.ajouter_serie(Serie(86, 10))
    exo.ajouter_serie(Serie(86, 10))
    seance.ajouter_exercice(exo)

    exo = ExerciceRealise(carnet.exercices["PO01"])
    exo.ajouter_serie(Serie(54, 15))
    exo.ajouter_serie(Serie(54, 13))
    exo.ajouter_serie(Serie(54, 12))
    seance.ajouter_exercice(exo)

    exo = ExerciceRealise(carnet.exercices["RM01"])
    exo.ajouter_serie(Serie(64, 14))
    exo.ajouter_serie(Serie(64, 13))
    exo.ajouter_serie(Serie(64, 12))
    seance.ajouter_exercice(exo)

    exo = ExerciceRealise(carnet.exercices["CP01"])
    exo.ajouter_serie(Serie(51, 15))
    exo.ajouter_serie(Serie(51, 13))
    exo.ajouter_serie(Serie(51, 11))
    seance.ajouter_exercice(exo)

    exo = ExerciceRealise(carnet.exercices["CU01"])
    exo.ajouter_serie(Serie(20, 13))
    exo.ajouter_serie(Serie(20, 11))
    exo.ajouter_serie(Serie(20, 10))
    seance.ajouter_exercice(exo)

    exo = ExerciceRealise(carnet.exercices["EA01"])
    exo.ajouter_serie(Serie(9, 20))
    exo.ajouter_serie(Serie(9, 18))
    exo.ajouter_serie(Serie(9, 16))
    seance.ajouter_exercice(exo)

    ajouter_si_absent(carnet, seance)

    seance = Seance("2026-06-11", 105)

    exo = ExerciceRealise(carnet.exercices["DC01"])
    exo.ajouter_serie(Serie(30, 13))
    exo.ajouter_serie(Serie(30, 10))
    exo.ajouter_serie(Serie(30, 9))
    seance.ajouter_exercice(exo)

    exo = ExerciceRealise(carnet.exercices["DI01"])
    exo.ajouter_serie(Serie(24, 13))
    exo.ajouter_serie(Serie(24, 12))
    exo.ajouter_serie(Serie(24, 10))
    seance.ajouter_exercice(exo)

    exo = ExerciceRealise(carnet.exercices["EP01"])
    exo.ajouter_serie(Serie(14, 15))
    exo.ajouter_serie(Serie(14, 13))
    exo.ajouter_serie(Serie(14, 10))
    seance.ajouter_exercice(exo)

    exo = ExerciceRealise(carnet.exercices["TD01"])
    exo.ajouter_serie(Serie(45, 20))
    exo.ajouter_serie(Serie(54, 15))
    exo.ajouter_serie(Serie(54, 13))
    seance.ajouter_exercice(exo)

    exo = ExerciceRealise(carnet.exercices["TE01"])
    exo.ajouter_serie(Serie(32, 14))
    exo.ajouter_serie(Serie(36, 13))
    exo.ajouter_serie(Serie(36, 12))
    seance.ajouter_exercice(exo)

    exo = ExerciceRealise(carnet.exercices["EL01"])
    exo.ajouter_serie(Serie(9, 20))
    exo.ajouter_serie(Serie(9, 18))
    exo.ajouter_serie(Serie(11, 15))
    exo.ajouter_serie(Serie(9, 18))
    seance.ajouter_exercice(exo)

    exo = ExerciceRealise(carnet.exercices["EA01"])
    exo.ajouter_serie(Serie(9, 20))
    exo.ajouter_serie(Serie(9, 18))
    exo.ajouter_serie(Serie(9, 16))
    seance.ajouter_exercice(exo)

    ajouter_si_absent(carnet, seance)

    seance = Seance("2026-06-12", 105)

    exo = ExerciceRealise(carnet.exercices["LE01"])
    exo.ajouter_serie(Serie(107, 13))
    exo.ajouter_serie(Serie(107, 11))
    exo.ajouter_serie(Serie(107, 10))
    seance.ajouter_exercice(exo)

    exo = ExerciceRealise(carnet.exercices["PR01"])
    exo.ajouter_serie(Serie(120, 13))
    exo.ajouter_serie(Serie(140, 12))
    exo.ajouter_serie(Serie(140, 10))
    seance.ajouter_exercice(exo)

    exo = ExerciceRealise(carnet.exercices["FS01"])
    exo.ajouter_serie(Serie(36, 10))
    exo.ajouter_serie(Serie(36, 10))
    exo.ajouter_serie(Serie(36, 10))
    seance.ajouter_exercice(exo)

    exo = ExerciceRealise(carnet.exercices["LC01"])
    exo.ajouter_serie(Serie(50, 15))
    exo.ajouter_serie(Serie(50, 13))
    exo.ajouter_serie(Serie(50, 11))
    seance.ajouter_exercice(exo)

    exo = ExerciceRealise(carnet.exercices["LA01"])
    exo.ajouter_serie(Serie(52, 13))
    exo.ajouter_serie(Serie(59, 12))
    exo.ajouter_serie(Serie(59, 10))
    seance.ajouter_exercice(exo)

    exo = ExerciceRealise(carnet.exercices["AD01"])
    exo.ajouter_serie(Serie(45, 20))
    exo.ajouter_serie(Serie(52, 13))
    exo.ajouter_serie(Serie(52, 11))
    seance.ajouter_exercice(exo)

    ajouter_si_absent(carnet, seance)


    carnet.sauvegarder("carnet.json")
    print(f"Séances ajoutées : {len(carnet.seances)} séance(s) dans le carnet.")


if __name__ == "__main__":
    ajouter_seances()