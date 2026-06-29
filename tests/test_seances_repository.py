import pytest
import sqlite3
from database.seances_repository import ajouter_seance, lister_seances, ajouter_exercice_realise_a_seance, lister_exercices_realises_par_seance, ajouter_serie, charger_seance_par_date, modifier_date_seance, prochain_numero, lister_series_par_exercice_realise, modifier_duree_seance, supprimer_seance, supprimer_toutes_les_seances, verifier_exercice_realise_existe


def test_ajouter_seance_apparait_dans_la_liste(conn):
    ajouter_seance(conn, "2026-06-24", 90)
    seances = lister_seances(conn)
    assert len(seances) == 1
    assert seances[0]["date"] == "2026-06-24"
    assert seances[0]["duree"] == 90

def test_ajouter_exercice_realise_apparait_dans_la_liste(conn_avec_catalogue):
    id_seance = ajouter_seance(conn_avec_catalogue, "2026-06-24", 90)
    ajouter_exercice_realise_a_seance(conn_avec_catalogue, id_seance, "DC01")
    ajouter_exercice_realise_a_seance(conn_avec_catalogue, id_seance, "DI01")
    exercices_realises = lister_exercices_realises_par_seance(conn_avec_catalogue, id_seance)
    assert len(exercices_realises) == 2
    assert exercices_realises[0]["nom"] == "Développé couché haltères"
    assert exercices_realises[1]["nom"] == "Développé incliné haltères"

def test_ajouter_serie_apparait_dans_la_liste(conn_avec_catalogue):
    id_seance = ajouter_seance(conn_avec_catalogue, "2026-06-24", 90)
    id_exo_realise = ajouter_exercice_realise_a_seance(conn_avec_catalogue, id_seance, "DC01")
    numero_serie_1 = prochain_numero(conn_avec_catalogue, id_exo_realise)
    ajouter_serie(conn_avec_catalogue, numero_serie_1, 90, 12, 0, id_exo_realise)
    numero_serie_2 = prochain_numero(conn_avec_catalogue, id_exo_realise)
    ajouter_serie(conn_avec_catalogue, numero_serie_2, 80, 14, 0, id_exo_realise)
    series = lister_series_par_exercice_realise(conn_avec_catalogue, id_exo_realise)
    assert len(series) == 2
    assert series[0]["poids"] == 90
    assert series[1]["reps"] == 14
    assert series[0]["numero_serie"] == 1
    assert series[1]["numero_serie"] == 2

def test_charger_seance_par_date_apparait(conn):
    ajouter_seance(conn, "2026-06-24", 90)
    seance = charger_seance_par_date(conn, "2026-06-24")
    assert seance is not None
    assert seance["date"] == "2026-06-24"

def test_modification_de_date_seance_apparait(conn):
    id_seance = ajouter_seance(conn, "2026-06-24", 90)
    modifier_date_seance(conn, id_seance, "2026-06-25")
    seance = lister_seances(conn)
    assert seance[0]["date"] == "2026-06-25"

def test_modification_duree_seance_apparait(conn):
    id_seance = ajouter_seance(conn, "2026-06-24", 90)
    modifier_duree_seance(conn, id_seance, 80)
    seance = lister_seances(conn)
    assert seance[0]["duree"] == 80

def test_supprimer_seances_effaces_toutes_les_seances(conn):
    ajouter_seance(conn, "2026-06-24", 90)
    ajouter_seance(conn, "2026-06-25", 90)
    supprimer_toutes_les_seances(conn)
    seances = lister_seances(conn)
    assert len(seances) == 0

def test_supprimer_seance_supprime_bien_la_seance_et_donnees_quelle_contient(conn_avec_catalogue):
    id_seance = ajouter_seance(conn_avec_catalogue, "2026-06-24", 90)
    id_exo_realise = ajouter_exercice_realise_a_seance(conn_avec_catalogue, id_seance, "DC01")
    numero_serie_1 = prochain_numero(conn_avec_catalogue, id_exo_realise)
    ajouter_serie(conn_avec_catalogue, numero_serie_1, 90, 12, 0, id_exo_realise)
    numero_serie_2 = prochain_numero(conn_avec_catalogue, id_exo_realise)
    ajouter_serie(conn_avec_catalogue, numero_serie_2, 80, 14, 0, id_exo_realise)
    supprimer_seance(conn_avec_catalogue, id_seance)
    seance = lister_seances(conn_avec_catalogue)
    assert len(seance) == 0
    assert not verifier_exercice_realise_existe(conn_avec_catalogue, id_exo_realise)
    assert len(lister_series_par_exercice_realise(conn_avec_catalogue, id_exo_realise)) == 0