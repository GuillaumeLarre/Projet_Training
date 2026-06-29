import pytest
import sqlite3
from database.schema import creer_tables
from database.exercices_repository import ajouter_exercice

@pytest.fixture
def conn():
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    creer_tables(conn)
    yield conn
    conn.close()

@pytest.fixture
def conn_avec_catalogue(conn):
    ajouter_exercice(conn, "DC01", "Développé couché haltères", "pectoraux", "haltères", ["portion médiane des pecs", "triceps", "deltoide antérieur"])
    ajouter_exercice(conn, "DI01", "Développé incliné haltères", "pectoraux", "haltères", ["portion supérieure des pecs", "deltoide antérieur", "triceps"])
    yield conn