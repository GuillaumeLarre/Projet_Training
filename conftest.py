import pytest
from database.exercices_repository import ajouter_exercice
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from database.models import Base

@pytest.fixture
def session():
    engine_test = create_engine("sqlite:///:memory:")
    @event.listens_for(engine_test, "connect")
    def _enable_fk(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.close()
    Base.metadata.create_all(engine_test)
    with Session(engine_test) as session:
        yield session

@pytest.fixture
def session_avec_catalogue(session):
    ajouter_exercice(session, "DC01", "Développé couché haltères", "pectoraux", "haltères", ["portion médiane des pecs", "triceps", "deltoide antérieur"])
    ajouter_exercice(session, "DI01", "Développé incliné haltères", "pectoraux", "haltères", ["portion supérieure des pecs", "deltoide antérieur", "triceps"])
    yield session