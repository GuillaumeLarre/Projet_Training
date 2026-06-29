from collections import defaultdict
from datetime import datetime
from constantes.constantes import FOURCHETTE_SERIES_SEMAINE
from fonctions_utiles.fonctions import nb_series_de_travail, volume_total_exercice_realise


def volume_total_par_groupe_musculaire_seance(seance) -> dict[str, float]:
    volume_par_groupe_par_seance = defaultdict(float)
    for exercice_realise in seance["exercices_realises"]:
        volume_par_groupe_par_seance[exercice_realise["groupe_musculaire"]] += volume_total_exercice_realise(exercice_realise)
    return volume_par_groupe_par_seance

def volume_total_par_groupe_musculaire(seances) -> dict[str, float]:
    volume_par_groupe = defaultdict(float)
    for seance in seances:
        for exercice_realise in seance["exercices_realises"]:
            volume_par_groupe[exercice_realise["groupe_musculaire"]] += volume_total_exercice_realise(exercice_realise)
    return volume_par_groupe

def nb_series_par_groupe_et_par_muscle_cible_par_semaine(seances) -> tuple[dict[tuple[int, int, str], int], dict[tuple[int, int, str], int]]:
    nb_series_par_groupe = defaultdict(int)
    nb_series_par_muscle_cible = defaultdict(int)
    for seance in seances:
        date_string = seance["date"]
        date_objet = datetime.strptime(date_string, "%Y-%m-%d")
        annee, num_semaine, jour = date_objet.isocalendar()
        for exercice_realise in seance["exercices_realises"]:
            nb_series_effectives = nb_series_de_travail(exercice_realise)
            nb_series_par_groupe[(annee, num_semaine, exercice_realise["groupe_musculaire"])] += nb_series_effectives
            for muscle_cible in exercice_realise["muscles_cibles"]:
                nb_series_par_muscle_cible[(annee, num_semaine, muscle_cible)] += nb_series_effectives
    return nb_series_par_groupe, nb_series_par_muscle_cible

def lister_exercices_differents_par_groupe(seances) -> dict[str, list[str]]:
    liste_exercices_differents_par_groupe = defaultdict(set)
    for seance in seances:
        for exercice_realise in seance["exercices_realises"]:
            liste_exercices_differents_par_groupe[exercice_realise["groupe_musculaire"]].add(exercice_realise["nom"])
    return {groupe : sorted(exos) for groupe, exos in liste_exercices_differents_par_groupe.items()}

def frequence_groupe_et_par_muscle_par_semaine(seances) -> tuple[dict[tuple[int, int, str], int], dict[tuple[int, int, str], int]]:
    frequence_par_groupe_par_semaine = defaultdict(int)
    frequence_par_muscle_par_semaine = defaultdict(int)
    for seance in seances:
        date_string = seance["date"]
        date_objet = datetime.strptime(date_string, "%Y-%m-%d")
        annee, num_semaine, jour = date_objet.isocalendar()
        groupe_unique = set()
        muscle_cible_unique = set()
        for exercice_realise in seance["exercices_realises"]:
            groupe_unique.add(exercice_realise["groupe_musculaire"])
            for muscle in exercice_realise["muscles_cibles"]:
                muscle_cible_unique.add(muscle)
        for groupe in groupe_unique:
            frequence_par_groupe_par_semaine[(annee, num_semaine, groupe)] += 1
        for muscle_cible in muscle_cible_unique:
            frequence_par_muscle_par_semaine[(annee, num_semaine, muscle_cible)] += 1
    return frequence_par_groupe_par_semaine, frequence_par_muscle_par_semaine

def un_rm_estime_par_exercice(seances) -> dict[str, float]:
    records = defaultdict(float)
    for seance in seances:
        for exercice_realise in seance["exercices_realises"]:
            nom = exercice_realise["nom"]
            for serie in exercice_realise["series"]:
                if not serie["est_echauffement"]:
                    poids = serie["poids"]
                    reps = serie["reps"]
                    rm = poids * (1 + reps / 30)
                    if rm > records[nom]:
                        records[nom] = rm
    return {nom: round(rm, 1) for nom, rm in records.items()}

def comparaison_nb_series_par_groupe_et_fourchette_scientifique(seances) -> dict[tuple[int, int, str], dict]:
    nb_series_par_groupe, _ = nb_series_par_groupe_et_par_muscle_cible_par_semaine(seances)
    comparaison_fourchettes_scientifiques = {}
    for (annee, semaine, groupe), nb_series in nb_series_par_groupe.items():
        if groupe in FOURCHETTE_SERIES_SEMAINE:
            basse, optimum, haute = FOURCHETTE_SERIES_SEMAINE[groupe]
            if nb_series < basse:
                statut = "insuffisant"
            elif basse <= nb_series < optimum:
                statut = "fourchette basse"
            elif optimum <= nb_series < haute:
                statut = "optimum"
            else:
                statut = "fourchette haute"
            comparaison_fourchettes_scientifiques[(annee, semaine, groupe)] = {"nb_series": nb_series, "statut": statut}
    return comparaison_fourchettes_scientifiques
        
def evolution_des_charges_dans_le_temps(seances) -> dict[str, list[tuple[str, float]]]:
    regroupement_record_poids_par_exercice_et_par_seance = defaultdict(list)
    for seance in seances:
        for exercice_realise in seance["exercices_realises"]:
            record_local = 0.0
            for serie in exercice_realise["series"]:
                if not serie["est_echauffement"]:
                    if serie["poids"] > record_local:
                        record_local = serie["poids"]
            if record_local > 0:
                regroupement_record_poids_par_exercice_et_par_seance[exercice_realise["nom"]].append((seance["date"], record_local))
    return {nom: sorted(liste) for nom, liste in regroupement_record_poids_par_exercice_et_par_seance.items()}

def liste_exercices_pratiques(seances) -> list:
    liste_ids = set()
    for seance in seances:
        for exercice_realise in seance["exercices_realises"]:
            liste_ids.add(exercice_realise["id_exercice"])
    return list(liste_ids)

def record_par_exercice(id_exercice, seances) -> float:
    record = 0.0
    for seance in seances:
        for exercice_realise in seance["exercices_realises"]:
            if exercice_realise["id_exercice"] == id_exercice:
                for serie in exercice_realise["series"]:
                    if not serie["est_echauffement"]:
                        poids = serie["poids"]
                        if poids > record:
                            record = poids
    return record