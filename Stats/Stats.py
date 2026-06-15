from collections import defaultdict
from datetime import datetime
from constantes.constantes import FOURCHETTE_SERIES_SEMAINE
from models.Seance import Seance
from models.CarnetEntrainement import CarnetEntrainement


def volume_total_par_groupe_musculaire_seance(seance: Seance) -> dict[str, float]:
    volume_par_groupe_par_seance = defaultdict(float)
    for exercice_realise in seance.exercices_realises:
        volume_par_groupe_par_seance[exercice_realise.exercice.groupe_musculaire] += exercice_realise.volume_total
    return volume_par_groupe_par_seance

def volume_total_par_groupe_musculaire(carnet: CarnetEntrainement) -> dict[str, float]:
    volume_par_groupe = defaultdict(float)
    for seance in carnet.seances:
        for exercice_realise in seance.exercices_realises:
            volume_par_groupe[exercice_realise.exercice.groupe_musculaire] += exercice_realise.volume_total
    return volume_par_groupe

def nb_series_par_groupe_et_par_muscle_cible_par_semaine(carnet: CarnetEntrainement) -> tuple[dict[tuple[int, int, str], int], dict[tuple[int, int, str], int]]:
    nb_series_par_groupe = defaultdict(int)
    nb_series_par_muscle_cible = defaultdict(int)
    for seance in carnet.seances:
        date_string = seance.date
        date_objet = datetime.strptime(date_string, "%Y-%m-%d")
        annee, num_semaine, jour = date_objet.isocalendar()
        for exercice_realise in seance.exercices_realises:
            nb_series_par_groupe[(annee, num_semaine, exercice_realise.exercice.groupe_musculaire)] += exercice_realise.nb_series
            for muscle_cible in exercice_realise.exercice.muscle_cible:
                nb_series_par_muscle_cible[(annee, num_semaine, muscle_cible)] += exercice_realise.nb_series
    return nb_series_par_groupe, nb_series_par_muscle_cible

def lister_exercices_differents_par_groupe(carnet: CarnetEntrainement) -> dict[str, list[str]]:
    liste_exercices_differents_par_groupe = defaultdict(set)
    for seance in carnet.seances:
        for exercice_realise in seance.exercices_realises:
            liste_exercices_differents_par_groupe[exercice_realise.exercice.groupe_musculaire].add(exercice_realise.exercice.nom)
    return {groupe : sorted(exos) for groupe, exos in liste_exercices_differents_par_groupe.items()}

def frequence_groupe_et_par_muscle_par_semaine(carnet: CarnetEntrainement) -> tuple[dict[tuple[int, int, str], int], dict[tuple[int, int, str], int]]:
    frequence_par_groupe_par_semaine = defaultdict(int)
    frequence_par_muscle_par_semaine = defaultdict(int)
    for seance in carnet.seances:
        date_string = seance.date
        date_objet = datetime.strptime(date_string, "%Y-%m-%d")
        annee, num_semaine, jour = date_objet.isocalendar()
        groupe_unique = set()
        muscle_cible_unique = set()
        for exercice_realise in seance.exercices_realises:
            groupe_unique.add(exercice_realise.exercice.groupe_musculaire)
            for muscle in exercice_realise.exercice.muscle_cible:
                muscle_cible_unique.add(muscle)
        for groupe in groupe_unique:
            frequence_par_groupe_par_semaine[(annee, num_semaine, groupe)] += 1
        for muscle_cible in muscle_cible_unique:
            frequence_par_muscle_par_semaine[(annee, num_semaine, muscle_cible)] += 1
    return frequence_par_groupe_par_semaine, frequence_par_muscle_par_semaine

def un_rm_estime_par_exercice(carnet: CarnetEntrainement) -> dict[str, float]:
    records = defaultdict(float)
    for seance in carnet.seances:
        for exercice_realise in seance.exercices_realises:
            nom = exercice_realise.exercice.nom
            for serie in exercice_realise.series:
                if not serie.est_echauffement:
                    poids = serie.poids
                    reps = serie.reps
                    rm = poids * (1 + reps / 30)
                    if rm > records[nom]:
                        records[nom] = rm
    return {nom: round(rm, 1) for nom, rm in records.items()}

def comparaison_nb_series_par_groupe_et_fourchette_scientifique(carnet: CarnetEntrainement) -> dict[tuple[int, int, str], dict]:
    nb_series_par_groupe, _ = nb_series_par_groupe_et_par_muscle_cible_par_semaine(carnet)
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
        
def evolution_des_charges_dans_le_temps(carnet: CarnetEntrainement) -> dict[str, list[tuple[str, float]]]:
    regroupement_record_poids_par_exercice_et_par_seance = defaultdict(list)
    for seance in carnet.seances:
        for exercice_realise in seance.exercices_realises:
            record_local = 0.0
            for serie in exercice_realise.series:
                if not serie.est_echauffement:
                    if serie.poids > record_local:
                        record_local = serie.poids
            if record_local > 0:
                regroupement_record_poids_par_exercice_et_par_seance[exercice_realise.exercice.nom].append((seance.date, record_local))
    return {nom: sorted(liste) for nom, liste in regroupement_record_poids_par_exercice_et_par_seance.items()}
