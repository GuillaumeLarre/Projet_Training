import pytest
from models.Serie import Serie
from models.Exercice import Exercice
from models.ExerciceRealise import ExerciceRealise
from models.Seance import Seance
from models.CarnetEntrainement import CarnetEntrainement
from stats.stats import (
    volume_total_par_groupe_musculaire,
    un_rm_estime_par_exercice,
    nb_series_par_groupe_et_par_muscle_cible_par_semaine,
)
def faire_carnet_simple():
    exo = Exercice("LE01", "Leg extension", "jambes", ["quadriceps"], "machine")
    seance = Seance("2026-06-01", 60)
    ex_r = ExerciceRealise(exo)
    ex_r.ajouter_serie(Serie(50, 10))
    ex_r.ajouter_serie(Serie(60, 8))
    seance.ajouter_exercice(ex_r)
    carnet = CarnetEntrainement()
    carnet.ajouter_exercice(exo)
    carnet.ajouter_seance(seance)
    return carnet


def test_volume_total_par_groupe_carnet_simple():
    carnet = faire_carnet_simple()
    resultat = volume_total_par_groupe_musculaire(carnet)
    assert resultat["jambes"] == 980


def test_un_rm_estime_formule_epley():
    carnet = faire_carnet_simple()
    resultat = un_rm_estime_par_exercice(carnet)
    assert resultat["Leg extension"] == 76.0
    # Formule 1rm = poids * (1 + reps/30) #
    # Série 1: 76 #
    # Série 2: 66.7 #

def test_nb_series_ignore_echauffement():
    exo = Exercice("LE01", "Leg extension", "jambes", ["quadriceps"], "machine")
    seance = Seance("2026-06-01", 60)
    ex_r = ExerciceRealise(exo)
    ex_r.ajouter_serie(Serie(20, 15, est_echauffement=True))
    ex_r.ajouter_serie(Serie(50, 10))
    ex_r.ajouter_serie(Serie(60, 8))
    seance.ajouter_exercice(ex_r)
    
    carnet = CarnetEntrainement()
    carnet.ajouter_exercice(exo)
    carnet.ajouter_seance(seance)
    
    nb_par_groupe, _ = nb_series_par_groupe_et_par_muscle_cible_par_semaine(carnet)
    # 2026-06-01 est en semaine 23 de 2026
    assert nb_par_groupe[(2026, 23, "jambes")] == 2