import pytest
from models.Serie import Serie
from models.Exercice import Exercice
from models.ExerciceRealise import ExerciceRealise

def faire_exo_machine():
    return Exercice("LE01", "Leg extension", "jambes", ["quadriceps"], "machine")

def faire_exo_halteres():
    return Exercice("DC01", "DC haltères", "pectoraux", ["portion médiane des pecs", "triceps", "deltoide antérieur"], "haltères")

def test_volume_total_machine_sans_echauffement():
    exo = faire_exo_machine()
    ex_r = ExerciceRealise(exo)
    ex_r.ajouter_serie(Serie(50, 10))   # 500
    ex_r.ajouter_serie(Serie(60, 8))    # 480
    assert ex_r.volume_total == 980

def test_volume_total_halteres_multiplie_par_2():
    exo = faire_exo_halteres()
    ex_r = ExerciceRealise(exo)
    ex_r.ajouter_serie(Serie(30, 10))   # 300 × 2 = 600
    assert ex_r.volume_total == 600

def test_volume_total_exclut_echauffement():
    exo = faire_exo_machine()
    ex_r = ExerciceRealise(exo)
    ex_r.ajouter_serie(Serie(20, 15, est_echauffement=True))
    ex_r.ajouter_serie(Serie(50, 10))                          # 500
    ex_r.ajouter_serie(Serie(60, 8))                           # 480
    assert ex_r.volume_total == 980

def test_volume_total_halteres_et_echauffement():
    exo = faire_exo_halteres()
    ex_r = ExerciceRealise(exo)
    ex_r.ajouter_serie(Serie(10, 15, est_echauffement=True))
    ex_r.ajouter_serie(Serie(30, 10))                          # 300 × 2 = 600
    assert ex_r.volume_total == 600

def test_volume_total_aucune_serie():
    exo = faire_exo_machine()
    ex_r = ExerciceRealise(exo)
    assert ex_r.volume_total == 0

def test_nb_series_simple():
    exo = faire_exo_machine()
    ex_r = ExerciceRealise(exo)
    ex_r.ajouter_serie(Serie(50, 10))
    ex_r.ajouter_serie(Serie(60, 8))
    ex_r.ajouter_serie(Serie(70, 6))
    assert ex_r.nb_series == 3

def test_nb_series_exclut_echauffement():
    exo = faire_exo_machine()
    ex_r = ExerciceRealise(exo)
    ex_r.ajouter_serie(Serie(20, 15, est_echauffement=True))
    ex_r.ajouter_serie(Serie(30, 12, est_echauffement=True))
    ex_r.ajouter_serie(Serie(50, 10))
    ex_r.ajouter_serie(Serie(60, 8))
    assert ex_r.nb_series == 2

def test_nb_series_aucune_serie():
    exo = faire_exo_machine()
    ex_r = ExerciceRealise(exo)
    assert ex_r.nb_series == 0