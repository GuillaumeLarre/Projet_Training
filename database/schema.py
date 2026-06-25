import sqlite3

def creer_tables(conn) -> None:
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exercices (
            id_exercice TEXT PRIMARY KEY,
            nom TEXT NOT NULL,
            groupe_musculaire TEXT NOT NULL,
            type_materiel TEXT NOT NULL
            )
        """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS muscles_cibles_exercices (
            id_exercice TEXT NOT NULL,
            nom_muscle TEXT NOT NULL,
            PRIMARY KEY (id_exercice, nom_muscle),
            FOREIGN KEY (id_exercice) REFERENCES exercices (id_exercice)
            )
        """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS seances (
            id_seance INTEGER PRIMARY KEY,
            date DATE NOT NULL UNIQUE,
            duree INTEGER NOT NULL CHECK (duree > 0)
            )
        """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exercices_realises (
            id_exercice_realise INTEGER PRIMARY KEY,
            id_exercice TEXT NOT NULL,
            id_seance INTEGER NOT NULL,
            UNIQUE (id_exercice, id_seance),
            FOREIGN KEY (id_exercice) REFERENCES exercices (id_exercice),
            FOREIGN KEY (id_seance) REFERENCES seances (id_seance) ON DELETE CASCADE
            )
        """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS series (
            id_serie INTEGER PRIMARY KEY,
            numero_serie INTEGER NOT NULL,
            poids REAL NOT NULL CHECK (poids > 0),
            reps INTEGER NOT NULL CHECK (reps > 0),
            est_echauffement BOOLEAN NOT NULL DEFAULT 0 CHECK (est_echauffement IN (0, 1)),
            id_exercice_realise INTEGER NOT NULL,
            UNIQUE (numero_serie, id_exercice_realise),
            FOREIGN KEY (id_exercice_realise) REFERENCES exercices_realises (id_exercice_realise) ON DELETE CASCADE
            )
        """)