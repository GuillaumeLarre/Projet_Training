from models.Serie import Serie

import pytest 

def test_volume_simple():
    serie = Serie(30, 10)
    assert serie.volume == 300

def test_volume_avec_decimale():
    serie = Serie(22.5, 8)
    assert serie.volume == 180.0

def test_est_echauffement_defaut_false():
    serie = Serie(30, 10)
    assert serie.est_echauffement == False

def test_est_echauffement_explicite_true():
    serie = Serie(30, 10, est_echauffement=True)
    assert serie.est_echauffement == True

def test_poids_negatif_leve_erreur():
    with pytest.raises(ValueError):
        Serie(-10, 8)

def test_reps_zero_leve_erreur():
    with pytest.raises(ValueError):
        Serie(30, 0)

def test_to_dict():
    serie = Serie(30, 10, est_echauffement=True)
    attendu = {"poids": 30, "reps": 10, "est_echauffement": True}
    assert serie.to_dict() == attendu

def test_from_dict_avec_echauffement():
    donnees = {"poids": 30, "reps": 10, "est_echauffement": True}
    serie = Serie.from_dict(donnees)
    assert serie.poids == 30
    assert serie.reps == 10
    assert serie.est_echauffement == True

def test_from_dict_sans_echauffement_retrocompatible():
    donnees = {"poids": 30, "reps": 10}
    serie = Serie.from_dict(donnees)
    assert serie.est_echauffement == False