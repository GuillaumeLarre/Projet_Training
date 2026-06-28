from database.seances_repository import verifier_date_seance_existe, enregistrer_seance_complete
from database.exercices_repository import charger_catalogue
import sqlite3

def exo(id_exercice, *series_tuples):
    """Construit le dict d'un exercice réalisé à partir de tuples (poids, reps)."""
    return {
        "id_exercice": id_exercice,
        "series": [{"poids": p, "reps": r, "est_echauffement": 0} for p, r in series_tuples]
    }

def ajouter_seances():
    with sqlite3.connect("musculation.db") as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.row_factory = sqlite3.Row
        catalogue = charger_catalogue(conn) 
        if not catalogue:
            print("⚠️  Le catalogue est vide. Lance d'abord seed.py.")
            return
        seances = [
        {
            "date": "2026-06-08",
            "duree": 105,
            "exercices_realises": [
                exo("DC01", (30, 13), (30, 10), (30, 9)),
                exo("DI01", (24, 13), (24, 12), (24, 10)),
                exo("EP01", (14, 15), (14, 13), (14, 10)),
                exo("CP01", (51, 15), (51, 13), (51, 11)),
                exo("CU01", (20, 13), (20, 12), (20, 10)),
                exo("EL01", (9, 20), (9, 18), (11, 15), (9, 18)),
                exo("EA01", (9, 20), (9, 18), (9, 16)),
            ],
        },
        {
            "date": "2026-06-09",
            "duree": 105,
            "exercices_realises": [
                exo("LE01", (107, 13), (107, 11), (107, 10)),
                exo("HS01", (90, 13), (90, 11), (90, 10)),
                exo("PR01", (120, 13), (140, 12), (140, 10)),
                exo("LC01", (50, 15), (50, 13), (50, 11)),
                exo("LA01", (52, 13), (59, 12), (59, 10)),
                exo("AD01", (45, 20), (52, 13), (52, 11)),
            ],
        },
        {
            "date": "2026-06-10",
            "duree": 105,
            "exercices_realises": [
                exo("RV01", (73, 12), (73, 11), (73, 10)),
                exo("TV01", (86, 13), (86, 10), (86, 10)),
                exo("PO01", (54, 15), (54, 13), (54, 12)),
                exo("RM01", (64, 14), (64, 13), (64, 12)),
                exo("CP01", (51, 15), (51, 13), (51, 11)),
                exo("CU01", (20, 13), (20, 11), (20, 10)),
                exo("EA01", (9, 20), (9, 18), (9, 16)),
            ],
        },
        {
            "date": "2026-06-11",
            "duree": 105,
            "exercices_realises": [
                exo("DC01", (30, 13), (30, 10), (30, 9)),
                exo("DI01", (24, 13), (24, 12), (24, 10)),
                exo("EP01", (14, 15), (14, 13), (14, 10)),
                exo("TD01", (45, 20), (54, 15), (54, 13)),
                exo("TE01", (32, 14), (36, 13), (36, 12)),
                exo("EL01", (9, 20), (9, 18), (11, 15), (9, 18)),
                exo("EA01", (9, 20), (9, 18), (9, 16)),
            ],
        },
        {
            "date": "2026-06-12",
            "duree": 105,
            "exercices_realises": [
                exo("LE01", (107, 13), (107, 11), (107, 10)),
                exo("PR01", (120, 13), (140, 12), (140, 10)),
                exo("FS01", (36, 10), (36, 10), (36, 10)),
                exo("LC01", (50, 15), (50, 13), (50, 11)),
                exo("LA01", (52, 13), (59, 12), (59, 10)),
                exo("AD01", (45, 20), (52, 13), (52, 11)),
            ],
        },
    ]
        nb_ajoutees = 0
        for seance in seances:
            if verifier_date_seance_existe(conn, seance["date"]):
                print(f"⚠️ Séance déjà existante pour le {seance['date']}, ignorée.")
                continue
            enregistrer_seance_complete(conn, seance)
            nb_ajoutees += 1
        
        print(f"{nb_ajoutees} séance(s) ajoutée(s).")


if __name__ == "__main__":
    ajouter_seances()