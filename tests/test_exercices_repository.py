from database.exercices_repository import ajouter_exercice, charger_catalogue, verifier_id_exercice_existe, verifier_nom_exercice_deja_utilise
import pytest
import sqlite3

def test_ajouter_exercice_apparait_dans_catalogue(conn):
    ajouter_exercice(conn, "DC01", "Développé couché", "pectoraux", "barre", ["pec", "triceps"])
    catalogue = charger_catalogue(conn)
    assert "DC01" in catalogue
    assert catalogue["DC01"]["nom"] == "Développé couché"
    assert catalogue["DC01"]["groupe_musculaire"] == "pectoraux"
    assert catalogue["DC01"]["type_materiel"] == "barre"
    assert set(catalogue["DC01"]["muscles_cibles"]) == {"pec", "triceps"}

def test_verifier_id_exercice_existe(conn):
    ajouter_exercice(conn, "DC01", "Développé couché", "pectoraux", "barre", ["pec", "triceps"])
    assert verifier_id_exercice_existe(conn, "DC01")
    assert not verifier_id_exercice_existe(conn, "blabla")

def test_charger_catalogue_vide_retourne_dict_vide(conn):
    catalogue = charger_catalogue(conn)
    assert catalogue == {}

def test_ajouter_exercice_id_duplique_leve_erreur(conn):
    ajouter_exercice(conn, "DC01", "Développé couché", "pectoraux", "barre", ["pec", "triceps"])
    with pytest.raises(sqlite3.IntegrityError):
        ajouter_exercice(conn, "DC01", "Curl pupitre", "bras", "machine", ["biceps"])
    
def test_verifier_nom_exercice_deja_utilise(conn):
    ajouter_exercice(conn, "DC01", "Développé couché", "pectoraux", "barre", ["pec", "triceps"])
    assert verifier_nom_exercice_deja_utilise(conn, "Développé couché")
    assert not verifier_nom_exercice_deja_utilise(conn, "Squat libre")

def test_catalogue_avec_plusieurs_exercices(conn):
    ajouter_exercice(conn, "DC01", "Développé couché", "pectoraux", "barre", ["pec", "triceps"])
    ajouter_exercice(conn, "DC02", "Développé couché haltère", "pectoraux", "haltères", ["pec", "triceps"])
    catalogue = charger_catalogue(conn)
    assert len(catalogue) == 2
    assert "DC01" in catalogue
    assert "DC02" in catalogue
